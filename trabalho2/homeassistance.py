from dis import dis
import sys
import json
from time import sleep
from kafka import KafkaConsumer
from kafka import KafkaAdminClient
import threading
import socket 
from atuador import atuador_pb2
from atuador import atuador_pb2_grpc
import grpc

consumerGlobal = KafkaConsumer(bootstrap_servers='127.0.0.1:9092')

lock = threading.Lock() #Lock da listadeSensores
lock2 = threading.Lock() #Lock da lista de dispositivos

listasensores = []

admin_client = KafkaAdminClient(bootstrap_servers=['127.0.0.1:9092']) 

### --- PARA O SERVIDOR WEB --- ###
class Device:
    def __init__(self, name):
        self.topicOwner = name
        self.data = None

listaDispositivos = []
###### ------------------------ ######

arcondicionado = Device("Arcondicionado")
arcondicionado.data = '{"id": "1", "nome": "Arcondicionado", "valor": "0", "status": "desligado"}'
listaDispositivos.append(arcondicionado)
lampada = Device("Lampada")
lampada.data = '{"id": "2", "nome": "Lampada", "valor": "0", "status": "desligado"}'
listaDispositivos.append(lampada)
humidificador = Device("Humidificador")
humidificador.data = '{"id": "1", "nome": "Humidificador", "valor": "0", "status": "desligado"}'
listaDispositivos.append(humidificador)



def consumidorSensor(topico):
    print(f'Iniciada a thread do {topico}')
    consumer = KafkaConsumer(topico, bootstrap_servers='127.0.0.1:9092', auto_offset_reset="latest"
                            , value_deserializer = lambda value: json.loads(value), consumer_timeout_ms=20000)

    device = Device(topico)
    with lock2:
        listaDispositivos.append(device)

    try:
        for message in consumer:
            device.data = message.value


            #data : dict = message.value
            #print("Registro: ", data)
            
            sleep(3)
    except Exception as e:
        print(e)
        print("Thread do Sensor falhou, verifique o erro!")
    except KeyboardInterrupt:
        pass
    

    consumer.close()
    admin_client.delete_topics(topics=[f'{topico}'])
    with lock:
        listasensores.remove(topico)
    with lock2:
        listaDispositivos.remove(device)
    print(f'Excluido topico {topico}')

def verificaSensores():
    while True:
        try:
            listadetopicos = consumerGlobal.topics()

            with lock:
                listadetopicos = list(set(listadetopicos) - set(listasensores))

            for topico in listadetopicos:
                device_thread = threading.Thread(target=consumidorSensor,args=(topico,),daemon=True)
                device_thread.start()

                listasensores.append(topico)

            sleep(8) #verifica novos dispositivos cada 'x' segundos!
        except Exception as e:
            print(e)
            break
        except KeyboardInterrupt:
            break

def envioDeDispositivos():
    while True:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("127.0.0.1",2233))
        print("--- 127.0.0.1:2233 ---")
        server.listen()
        client, address = server.accept()
        print("Accepted web API")

        while True:
            try:

                print("Esperando comando do WebServer")

                comando = client.recv(2048).decode("utf-8")
                comando = comando.split('|')
                if not comando: 
                    print("Conexão com Webserver Perdida")
                    break
                
                mensagem = []

                if(comando[0] == '1'): #Retorna dispositivos

                    with lock2:
                        lista = listaDispositivos.copy()
                    for device in lista:
                        mensagem.append(device.data)
                    
                    try:
                        mensagem= '|'.join(mensagem)
                    except:
                        mensagem = 'none'

                    client.send(bytes(mensagem, encoding="utf-8"))

                    print("enviado dados dos sensores...")

                elif(comando[0] == '2'):
                    ArCondicionado(comando[1])
                    mensagem = "Success"

                    client.send(bytes(mensagem, encoding="utf-8"))
                
                elif(comando[0] == '3'):
                    Lampada(comando[1])
                    mensagem = "Success"

                    client.send(bytes(mensagem, encoding="utf-8"))

                elif(comando[0] == '4'):
                    Humidificador(comando[1])
                    mensagem = "Success"

                    client.send(bytes(mensagem, encoding="utf-8"))

                else:
                    print("Erro na API")
                    break

            except Exception as e:
                print(e)
                mensagem = "Fail!"

                client.send(bytes(mensagem, encoding="utf-8"))
                break
            except KeyboardInterrupt:
                break

def ArCondicionado(grpc_call):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = atuador_pb2_grpc.AtuadorGRPCStub(channel)

        if (grpc_call == '1'): #ligar
            ar_request = atuador_pb2.ArCondicionadoRequest()
            ar_reply = stub.ligarArCondicionado(ar_request)
            arcondicionado.data = '{"id": "1", "nome": "Arcondicionado", "valor": "' + f'{ar_reply.valor}' + '", "status": "ligado"}'
            print(ar_reply)
        
        if (grpc_call == '2'): #desligar
            arcondicionado.data = '{"id": "1", "nome": "Arcondicionado", "valor": "0", "status": "desligado"}'
            ar_request = atuador_pb2.ArCondicionadoRequest()
            ar_reply = stub.desligarArCondicionado(ar_request)
            print(ar_reply)
        
        if (grpc_call == '3'): #aumentar temperatura em 1
            ar_request = atuador_pb2.ArCondicionadoRequest()
            ar_reply = stub.aumentarTemperatura(ar_request)
            arcondicionado.data = '{"id": "1", "nome": "Arcondicionado", "valor": "' + f'{ar_reply.valor}' + '", "status": "ligado"}'
            print(ar_reply)
        
        if (grpc_call == '4'): #diminuir temperatura em 1
            ar_request = atuador_pb2.ArCondicionadoRequest()
            ar_reply = stub.diminuirTemperatura(ar_request)
            arcondicionado.data = '{"id": "1", "nome": "Arcondicionado", "valor": "' + f'{ar_reply.valor}' + '", "status": "ligado"}'
            print(ar_reply)
def Lampada(grpc_call):
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = atuador_pb2_grpc.AtuadorGRPCStub(channel)

        if (grpc_call == '1'):
            lampada.data = '{"id": "2", "nome": "Lampada", "valor": "99", "status": "ligado"}'
            lampada_request = atuador_pb2.LampadaRequest()
            lampada_reply = stub.ligarLampada(lampada_request)
            print(lampada_reply)
        
        if (grpc_call == '2'):
            lampada.data = '{"id": "2", "nome": "Lampada", "valor": "99", "status": "desligado"}'
            lampada_request = atuador_pb2.LampadaRequest()
            lampada_reply = stub.desligarLampada(lampada_request)
            print(lampada_reply)
def Humidificador(grpc_call):
    with grpc.insecure_channel('localhost:50053') as channel:
        stub = atuador_pb2_grpc.AtuadorGRPCStub(channel)

        if (grpc_call == '1'):
            humidificador.data = '{"id": "1", "nome": "Humidificador", "valor": "0", "status": "ligado"}'
            humidificador_request = atuador_pb2.HumidificadorRequest()
            humidificador_reply = stub.ligarHumidificador(humidificador_request)
            print(humidificador_reply)
        
        if (grpc_call == '2'):
            humidificador.data = '{"id": "1", "nome": "Humidificador", "valor": "0", "status": "desligado"}'
            humidificador_request = atuador_pb2.HumidificadorRequest()
            humidificador_reply = stub.desligarHumidificador(humidificador_request)
            print(humidificador_reply)

print("---INICIANDO HOMEASSISTANCE---")
thread1 = threading.Thread(target=envioDeDispositivos,args=(),daemon=True)
thread1.start()
thread2 = threading.Thread(target=verificaSensores,args=(),daemon=True)
thread2.start()


while True: #Thread Principal, existe para poder encerrar o processo com CTRL + C, visto que server.accept() trava o sinal de KeyboardInterrupt.
    try:
        sleep(10)
    except KeyboardInterrupt:
        print("Encerrando o HomeAssistance!")
        sys.exit(0)