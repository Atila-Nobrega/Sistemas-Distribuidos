import random
import re
import sys
import grpc
import time
from concurrent import futures

from atuador import atuador_pb2
from atuador import atuador_pb2_grpc




atuador = atuador_pb2.ArCondicionadoResponse()
atuador.id = int(random.randrange(500))
atuador.nome = "ar_condicionado"
atuador.status = True
atuador.valor = 24.0

class ServerArCondicionado(atuador_pb2_grpc.AtuadorGRPCServicer):

    def __init__(self) -> None:
        super().__init__()

    def ligarArCondicionado(self, request, context):
            
            

            to_txt = f"{atuador.valor}"

            with open("temperatura.txt", 'w') as f:
                f.write(to_txt)
            f.close()
            return atuador

    def desligarArCondicionado(self, request, context):
            
            atuador.status = False

            to_txt = f"{atuador.valor}"

            with open("temperatura.txt", 'w') as f:
                f.write(to_txt)
            f.close()
            return atuador
    def aumentarTemperatura(self, request, context):
            

            atuador.status = True

            valor = atuador.valor
            to_txt = f"{atuador.valor}"
            with open("temperatura.txt", 'w') as f:
                f.write(to_txt)
            f.close()

            while(valor < atuador.valor + 0.8):
                f = open('temperatura.txt', 'r')
                valor = float(str(f.read()))
                f.close()
                valor = valor + 0.2
                to_txt = f"{valor}"
                
                with open("temperatura.txt", 'w') as f:
                
                    f.write(to_txt)
                
                f.close()
                
                time.sleep(5)
            atuador.valor = valor
            return atuador


    def diminuirTemperatura(self, request, context):
            

            valor = atuador.valor
            to_txt = f"{atuador.valor}"
            with open("temperatura.txt", 'w') as f:
                f.write(to_txt)
            f.close()
    
            while(valor > atuador.valor - 0.8):
                f = open('temperatura.txt', 'r')
                valor = float(str(f.read()))
                f.close()
                valor = valor - 0.2
                to_txt = f"{valor}"
                
                with open("temperatura.txt", 'w') as f:
                
                    f.write(to_txt)
                
                f.close()
                
                time.sleep(0.2)
            atuador.valor = valor
            return atuador

def serve():

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        atuador_pb2_grpc.add_AtuadorGRPCServicer_to_server(ServerArCondicionado(), server)
        server.add_insecure_port("localhost:50051")
        server.start()
        server.wait_for_termination()


if __name__ == "__main__":
    
    try:
        serve()
    except:
        print("Encerrando o servidor!")
        sys.exit(0)