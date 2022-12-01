import socket 
import threading 
import sys
from time import sleep
from datetime import datetime

HOST = input("HOST: ")
PORT = int(input("PORT: "))

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()
print(f'Servidor ligado e rodando no IP: {HOST}:{PORT}')

clients = []
usernames = []
counter = 0

#Lamport
def local_time(counter):
    return ' (LAMPORT_TIME={})'.format(counter)

def calc_recv_timestamp(recv_time_stamp, counter):
    return max(int(recv_time_stamp), counter) + 1

def event(counter):
    counter += 1
    print('Something happened in {} !'.\
            local_time(counter))
    return counter

####

def globalMessage(username, message):
    global counter
    for client in clients:
        counter += 1
        print(f'Sending message to {usernames[clients.index(client)]} at ' + local_time(counter))
        newmessage = f'{username} -> {message}' + f'||{counter}'
        client.send(newmessage.encode('ascii'))

def globalMessageNewUser(message):
    global counter
    for client in clients:
        counter += 1
        print(f'Sending message to {client.getpeername()} at ' + local_time(counter))
        newmessage = message + f'||{counter}'
        client.send(newmessage.encode('ascii'))

def usersConnectedMessage(client):
    usersconnected = ""
    n = 0
    for user in usernames:
        n = n + 1
        usersconnected += f'{n}) {user}\n'
    
    message = usersconnected + f'||{counter}'

    client.send(message.encode('ascii'))

def handleMessages(client):
    global counter
    while True:
        try: 
            receiveMessageFromClient = client.recv(2048).decode('ascii')
            receiveMessageFromClient, received_counter = receiveMessageFromClient.split('||')
            counter = calc_recv_timestamp(received_counter, counter)
            print('Received message from client at ' + local_time(counter))

            if(receiveMessageFromClient == '/usuarios' or receiveMessageFromClient == '/USUARIOS'):
                counter += 1
                print(f'Retornando lista usuarios conectados para: {usernames[clients.index(client)]} ' + local_time(counter))
                usersConnectedMessage(client)
            else:
                username = usernames[clients.index(client)]
                globalMessage(username, receiveMessageFromClient)

        except:
            if(client.fileno() == -1): #Porta já está fechada!
                break
            clientLeavedUsername = usernames[clients.index(client)]
            clients.remove(client)
            counter += 1
            print(f'Usuario {clientLeavedUsername} com IP {client.getpeername()} foi desconectado at ' + local_time(counter))
            client.close()
            message = f'{clientLeavedUsername} saiu do chat...'
            globalMessage(message)
            usernames.remove(clientLeavedUsername)

def initialConnection():
    global counter
    while True:
        try:
            client, address = server.accept()
            counter += 1
            print('New connection at ' + local_time(counter))
            counter += 1
            message = 'getUser' + f'||{counter}'
            client.send(message.encode('ascii'))
            print('User Requested at ' + local_time(counter))
            message = client.recv(2048).decode('ascii')
            username, received_counter = message.split('||')
            counter = calc_recv_timestamp(received_counter, counter)
            print('User received at ' + local_time(counter))
            counter += 1
            print(f"Nova Conexão: {address} >Usuario: {username} at " + local_time(counter))
            clients.append(client)
            usernames.append(username) #variavel dentro do vetor
            globalMessageNewUser(f'{username} entrou no chat!')
            user_thread = threading.Thread(target=handleMessages,args=(client,),daemon=True)
            user_thread.start()
        except Exception as e:
            print(e)
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