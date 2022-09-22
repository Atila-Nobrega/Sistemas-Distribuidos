import socket 
import threading 
import sys
from time import sleep

HOST = input("HOST: ")
PORT = int(input("PORT: "))

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print(f'Servidor ligado e rodando no IP: {HOST}:{PORT}')

clients = []
usernames = []

def globalMessage(message):
    for client in clients:
        client.send(message)

def usersConnectedMessage(client):
    usersconnected = ""
    n = 0
    for user in usernames:
        n = n + 1
        usersconnected += f'{n}) {user}\n'

    client.send(usersconnected.encode('ascii'))

def handleMessages(client):
    while True:
        try: 
            receiveMessageFromClient = client.recv(2048).decode('ascii')
            if(receiveMessageFromClient == '/usuarios' or receiveMessageFromClient == '/USUARIOS'):
                print(f'Retornando lista usuarios conectados para: {usernames[clients.index(client)]}')
                usersConnectedMessage(client)
            else:
                globalMessage(f'{usernames[clients.index(client)]} -> {receiveMessageFromClient}'.encode('ascii'))

        except:
            if(client.fileno() == -1): #Porta já está fechada!
                break
            clientLeavedUsername = usernames[clients.index(client)]
            clients.remove(client)
            print(f'Usuario {clientLeavedUsername} com IP {client.getpeername()} foi desconectado...')
            client.close()
            globalMessage(f'{clientLeavedUsername} saiu do chat...'.encode('ascii'))
            usernames.remove(clientLeavedUsername)

def initialConnection():
    while True:
        try:
            client, address = server.accept()
            client.send('getUser'.encode('ascii'))
            username = client.recv(2048).decode('ascii')
            print(f"Nova Conexão: {address} >Usuario: {username}")
            clients.append(client)
            usernames.append(username) #variavel dentro do vetor
            globalMessage(f'{username} entrou no chat!'.encode('ascii'))
            user_thread = threading.Thread(target=handleMessages,args=(client,),daemon=True)
            user_thread.start()
        except:
            pass

connection_listenner = threading.Thread(target=initialConnection,args=(),daemon=True)
connection_listenner.start()

while True: #Thread Principal, existe para poder encerrar o processo com CTRL + C, visto que server.accept() trava o sinal de KeyboardInterrupt.
    try:
        sleep(10)
    except:
        server.close()
        print("Encerrando o servidor!")
        sys.exit(0)