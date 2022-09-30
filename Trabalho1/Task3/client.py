import socket
import threading
import sys
from time import sleep
import _thread
import enum_type


 

multicast_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("[+] Multicast socket is open!")
print("[+] Waiting for device data")
try:
  raw_input          # Python 2
except NameError:
  raw_input = input  # Python 3


# This function fills in a Person message based on user input.
def PromptForDevice(device):
  device.id = int(raw_input("Enter person ID number: "))
  device.nome = raw_input("Enter name: ")

  ip = raw_input("Enter the ip address: ")
  porta = raw_input("Enter the port address: ")

  type = raw_input("Is this a actuator, sensor, or both? ")
  if type == "actuator":
    device.type = device_pb2.Device.ATUADOR
  elif type == "sensor":
    device.type = device_pb2.Device.SENSOR
  elif type == "both":
    device.type = device_pb2.Device.ATUADOR_E_SENSOR
  else:
    print("Unknown device type; leaving as default value.")


# Main procedure:  Reads the entire address book from a file,
#   adds one person based on user input, then writes it back out to the same
#   file.
device = device_pb2.Device()

# Add an address.
PromptForDevice(device.add())

multicast_socket.bind((device.ip, device.porta))
i = 0

data, _ = multicast_socket.recvfrom(1024)


multicast_socket.close()



TCP_HOST = data.split(":")[0]

TCP_PORT = int(data.split(":")[1])

tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((TCP_HOST, TCP_PORT))

if(device.tipo == enum_type.DeviceType.ATUADOR):
  i = 0

if(device.tipo == enum_type.DeviceType.SENOSR):
  i = 0

if(device.tipo == enum_type.DeviceType.SENSOR_E_ATUADOR):
  i = 0
