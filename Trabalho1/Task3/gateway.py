from asyncio import SendfileNotAvailableError
import socket
import struct
import threading 
import sys
from time import sleep
from proto import device_pb2
import tkinter as tk


root = tk.Tk()
S = tk.Scrollbar(root)
T = tk.Text(root, height=40, width=50)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.LEFT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)

MCAST_GRP = '228.0.0.8'
MCAST_PORT = 6789
HOST = 'localhost'
SERVER_ADDR = 'localhost:9999'
TCP_PORT = 9999



def initialConnection():
    while True:   
        ttl = 2
        sock = socket.socket(socket.AF_INET,
                            socket.SOCK_DGRAM,
                            socket.IPPROTO_UDP)
        sock.setsockopt(socket.IPPROTO_IP,
                        socket.IP_MULTICAST_TTL,
                        ttl)
        sock.sendto(SERVER_ADDR.encode(), (MCAST_GRP, MCAST_PORT))

        sock.close()


print(f'Gateway is on and running on IP: {MCAST_GRP}:{MCAST_PORT}')

clients = []
devices_addr = []





def handleDevices(client):#Minha ideia é ter um ENUM pra cada tipo de dispositivo que a gente vai criar
    #Ai a gente pode tratar pelo tipo aqui dentro
    while True:
        try: 


            msg = client.recv(1024)
            if(msg == b''):
                raise Exception('Mensagem vazia')
            if(msg != b''):
                device2 = device_pb2.Device()
                device2.ParseFromString(msg)
      
                T.insert(tk.END, f"{device2.__str__()}\n")

        except Exception as e:
            break


def connectDevices():
    while True:
        try:
            client, address = server.accept()
            
            client.send(f'getDevice|{address[0]}'.encode())
            totallen = client.recv(4)

            totallenRecv = struct.unpack('>I', totallen)[0]


            msg = client.recv(totallenRecv) 
            device = device_pb2.Device()
            device.ParseFromString(msg)
      
            T.insert(tk.END, f"{device.__str__()}\n")
            valores = [client, address]
            clients.append(valores)
            
            device_thread = threading.Thread(target=handleDevices,args=(client,),daemon=True)
            device_thread.start()
        except Exception as e:
            print(e)
            pass


def sendCommand():
    while True:
        try:
            sleep(1)
            request = input("Digite um comando: ")
            ip = input("Digite o ip:")
            porta = int(input("Digite a porta: "))
            request = f'{request}|{ip}|{porta}'
            for client in clients:
                if (client[1][0] == ip) & (client[1][1] == porta):
                    client[0].send(request.encode())
                    print('mensagem enviada')
                    if(request == 'shutdown'):
                        clients.remove[client]
            
        except Exception as e:
            print(e)
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, TCP_PORT))
server.listen()


connection_listenner = threading.Thread(target=initialConnection,args=(),daemon=True)
connection_listenner.start()
user_thread = threading.Thread(target=connectDevices,args=(),daemon=True)
user_thread.start()
input_thread = threading.Thread(target=sendCommand, daemon=True)
input_thread.start()



 #Thread Principal, existe para poder encerrar o processo com CTRL + C, visto que server.accept() trava o sinal de KeyboardInterrupt.
try:
    tk.mainloop()
except:
    server.close()
    del clients
    print("Encerrando o servidor!")
    sys.exit(0)