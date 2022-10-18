import socket
import threading
import sys
from time import sleep
import _thread

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Cliente está rodando!")

comando = ""
connection = False

while comando != '/ENTRAR' and comando != '/entrar':
    print("Digite /ENTRAR ou /entrar para se conectar ao Chat!")
    comando = input ()

while connection == False:
    ServerIP = input ("ServerIP: ")
    PORT = int(input("ServerPort: "))
    username = input('Escolha um nome de usuário: ')

    try:
        client.connect((ServerIP,PORT))
        print(f'Conectado com Sucesso ao IP {ServerIP}:{PORT}')
        connection = True
    except:
        print(f'Conexão inválida, por revise sua entrada: {ServerIP}:{PORT}')

print("Digite /usuarios ou /USUARIOS para ver quem está online!")
print("Digite /sair ou /SAIR para sair do chat!")

def receiveMessage():
    while True:
        try: 
            message = client.recv(2048).decode('ascii')
            if message=='getUser':
                client.send(username.encode('ascii')) #Servidor Recupera do cliente o username inserido
            else:
                print(message) #Print da mensagem recebida pelo servidor
        except:
            print("Thread receiveMessage encerrada!")
            break

def sendMessage():
    while True:
        try:
            mensagem = input()
            print ("\033[A\033[A") #Apaga o Input repetido
            if mensagem != "/sair" and mensagem != "/SAIR":
                client.send(mensagem.encode('ascii')) #Envia a mensagem para o Servidor
            else:
                _thread.interrupt_main()
        except UnicodeEncodeError:
            print("Erro no envio! Verifique se mensagem funciona com ascii")
        except:
            print("Thread sendMessage encerrada!")
            break

thread1 = threading.Thread(target=receiveMessage, args=(), daemon=True) #Receber mensagem
thread2 = threading.Thread(target=sendMessage,args=(), daemon=True) #Envio de mensagem

thread1.start()
thread2.start()


while True: #Thread Principal, existe para poder encerrar o processo com CTRL + C, visto que server.accept() trava o sinal de KeyboardInterrupt.
    try:
        sleep(2)
    except:
        print("Encerrando o Cliente!")
        client.close()
        sys.exit(0)