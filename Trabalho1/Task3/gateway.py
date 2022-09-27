import socket
import threading 
import sys
from time import sleep

MCAST_GRP = '228.0.0.8'
MCAST_PORT = 6789
SERVER_PORT = 9999
MSG = '9999'

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((MCAST_GRP, SERVER_PORT))
server.listen()

print(f'Gateway ligado e rodando no IP: {MCAST_GRP}:{SERVER_PORT}')

clients = []
devices_name = []
def discoveryDevices():
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((MCAST_GRP, MCAST_PORT))
        sock.sendto(bytes(MSG, 'utf-8'), (MCAST_GRP, MCAST_PORT))
        tcp_thread = threading.Thread(target=initialConnection,args=(),daemon=True)
        tcp_thread.start()
        sock.close()


def handleDevices(client):#Minha ideia é ter um ENUM pra cada tipo de dispositivo que a gente vai criar
    #Ai a gente pode tratar pelo tipo aqui dentro
    while True:
        try: 
            receiveMessageFromClient = client.recv(2048).decode('ascii')


        except:
            if(client.fileno() == -1): #Porta já está fechada!
                break
            DeviceLeavedUsername = devices_name[clients.index(client)]
            clients.remove(client)
            print(f'Dispositivo {DeviceLeavedUsername} com IP {client.getpeername()} foi desconectado...')
            client.close()
     


def initialConnection():
    while True:
        try:
            client, address = server.accept()
            client.send('getDevice'.encode('ascii'))
            device = client.recv(2048).decode('ascii')
            print(f"Nova Conexão: {address} >Usuario: {device}")
            clients.append(client)
            devices_name.append(device) #variavel dentro do vetor
            device_thread = threading.Thread(target=handleDevices,args=(client,),daemon=True)
            device_thread.start()
        except:
            pass

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


connection_listenner = threading.Thread(target=discoveryDevices,args=(),daemon=True)
connection_listenner.start()