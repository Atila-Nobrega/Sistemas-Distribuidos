import socket
import threading
import sys
from time import sleep
import _thread
import traceback
import enum_type
import struct
from proto import device_pb2
import binascii

MCAST_GRP = '228.0.0.8'
MCAST_PORT = 6789

print("[+] Multicast socket is open!")
print("[+] Waiting for device data")
try:
  raw_input          # Python 2
except NameError:
  raw_input = input  # Python 3


# This function fills in a Person message based on user input.
def PromptForDevice(device):
  device.id = int(raw_input("Enter device ID number: "))
  device.nome = input("Enter name: ")

  device.ip = input("Enter the ip address: ")
  device.porta = int(raw_input("Enter the port address: "))

  type = raw_input("Is this a actuator, sensor, or both? ")
  if type == "actuator":
    device.tipo = 0
  elif type == "sensor":
    device.tipo = 1
  elif type == "both":
    device.tipo = 2
  else:
    print("Unknown device type; leaving as default value.")

  device.ligado = True
  
  if(device.tipo == 1) | (device.tipo == 2):
    device.valor = 1.0

  return device

# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
device = device_pb2.Device()
print(device)
# Add an address.
device = PromptForDevice(device)
print(device.ip, ":", device.porta)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('', MCAST_PORT))
mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
data, _ = sock.recvfrom(10240)
print(sock.recv(10240))
sock.close()

data = data.decode()

TCP_HOST = data.split(":")[0]

TCP_PORT = int(data.split(":")[1])
print(TCP_HOST + ":" + str(TCP_PORT))

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("[+] Client is running!")

connection = False
while connection == False:
    try:
        client.bind((device.ip, device.porta))
        client.connect((TCP_HOST,TCP_PORT))
        
        print(f'Connected with sucess on IP {TCP_HOST}:{TCP_PORT}')
        connection = True
    except:
        print(f'Conexão inválida, por revise sua entrada: {TCP_HOST}:{TCP_PORT}')

def receiveMessage():
    while True:
        try: 
            message = client.recv(1024).decode()
            msg = message.split('|')[0]  
            ip = message.split('|')[1]

            if (msg== 'getDevice') and (device.ip == ip):
                device2 = device_pb2.Device()
                par = device.SerializeToString()
                device2.ParseFromString(par)
      
                totallen = len(device.SerializeToString())
                pack1 = struct.pack('>I', totallen) 
                client.sendall(pack1)
                client.sendall(device.SerializeToString()) 
                sleep(1)
            elif (msg== 'on') & (device.ip == ip):
                device.ligado == True
            elif (msg== 'shutdown') & (device.ip == ip):
                device.ligado == False
            elif (msg== 'disconnect') & (device.ip == ip):
                 _thread.interrupt_main()
            elif (msg== '-') & ((device.tipo == 1) | (device.tipo == 2)) &( device.ip == ip):
                device.valor -= 1
                print('Valor foi reduzido com sucesso')
            elif (msg== '+') & ((device.tipo == 1) | (device.tipo == 2)) & (device.ip == ip):
                device.valor += 1
                print('Valor foi aumentado com sucesso')

        except Exception as e:
            print(e)
            print(traceback.format_exc())
            break

def sendMessage():
    while True:
        try:
            if(device.tipo == 1) | (device.tipo == 2):
              sleep(20)

              client.send(device.SerializeToString()) 

        except UnicodeEncodeError:
            print("Erro no envio! Verifique se mensagem funciona com ascci")
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