import socket
import threading
import sys
from time import sleep
import _thread

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect(('127.0.0.1',2233))

client.send(bytes('1',encoding="utf-8"))

sleep(1)

mensagem = client.recv(2048).decode("utf-8")

if mensagem == 'none':
    print('nada')
else:
    print(mensagem)

client.send(bytes('2',encoding="utf-8"))

sleep(1)

mensagem = client.recv(2048).decode("utf-8")

if mensagem == 'none':
    print('nada')
else:
    print(mensagem)

sleep(10)