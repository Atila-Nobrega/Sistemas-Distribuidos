#from kafka.admin import NewTopic
from kafka import KafkaProducer
from kafka import KafkaAdminClient
import json
from time import sleep
from datetime import datetime

producer = KafkaProducer( bootstrap_servers=['127.0.0.1:9092'], value_serializer = lambda value: json.dumps(value).encode())

id = int(input("Enter device ID number: "))

while True:
    name = input("Defina o tipo de sensor (temperatura, luminosidade, humidade): ")

    if(name!= "temperatura" and name!= "luminosidade" and name!= "humidade"):
        pass
    else:
        break

print(f'Iniciando Sensor de {name}.')

value = 0 #Valor a ser posto no .txt!

#topic = NewTopic(name=f'{name}-{id}', num_partitions=1, replication_factor=1)
#admin_client.create_topics(new_topics=[topic], validate_only=False)

while True:
    try:
        f = open(f'{name}.txt', "r")
        value = f.read()
    except:
        print("Erro na leitura do arquivo de simulação!")

    time = datetime.now()

    dictionary = {
    "id": f'{id}',
    "nome": f'{name}',
    "valor": f'{value}',
    "Horario": f'{time}'
    }
    message = json.dumps(dictionary)

    try:
        print('Enviando leitura para o Kafka!')
        producer.send( f'{name}-{id}' , message)
        print('Okay!')


        sleep(5)
    except Exception as e:
        print(e)
        print("Erro no envio!")
        break
    except KeyboardInterrupt:
        print("CTRL-C encerrando...")
        break



