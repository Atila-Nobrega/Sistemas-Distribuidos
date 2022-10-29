from dis import dis
import sys
import json
from time import sleep
from kafka import KafkaConsumer
from kafka import KafkaAdminClient
import threading
import socket 

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
                if not comando: 
                    print("Conexão com Webserver Perdida")
                    break

                if(comando == '1'): #Retorna dispositivos

                    mensagem = []
                    with lock2:
                        lista = listaDispositivos.copy()
                    for device in lista:
                        mensagem.append(device.data)
                    
                    try:
                        mensagem= ', '.join(mensagem)
                    except:
                        mensagem = 'none'

                    client.send(bytes(mensagem, encoding="utf-8"))

                    print("enviado dados dos sensores...")

                elif(comando == '2'): #envia comando pro atuador...
                    pass

            except Exception as e:
                print(e)
                break
            except KeyboardInterrupt:
                break

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