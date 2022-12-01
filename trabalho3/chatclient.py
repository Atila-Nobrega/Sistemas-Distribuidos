import socket
import threading
import sys
from time import sleep
from datetime import datetime
import _thread
import traceback

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Cliente está rodando!")

comando = ""
connection = False


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

counter = 0
####


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
    global counter
    while True:
        try: 
            message = client.recv(2048).decode('ascii')
            message, received_counter = message.split('||')
            counter = calc_recv_timestamp(received_counter, counter)
            if message=='getUser':
                print('User request received at ' + local_time(counter))

                sleep(1)
                counter += 1
                usernamemessage = username + f'||{counter}'
                client.send(usernamemessage.encode('ascii')) #Servidor Recupera do cliente o username inserido
                print('Username sent at' + local_time(counter))
            else:
                print(message + ' ' + local_time(counter)) #Print da mensagem recebida pelo servidor
        except Exception as e:
            print(e)
            traceback.print_exc()
            print("Thread receiveMessage encerrada!")
            break

def sendMessage():
    global counter
    while True:
        try:
            mensagem = input()
            print ("\033[A\033[A") #Apaga o Input repetido
            if mensagem != "/sair" and mensagem != "/SAIR":
                counter += 1
                mensagem = mensagem + f'||{counter}'
                client.send(mensagem.encode('ascii')) #Envia a mensagem para o Servidor
                print('Message sent at' + local_time(counter))
            else:
                counter += 1
                print('Exiting ' + local_time(counter))
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