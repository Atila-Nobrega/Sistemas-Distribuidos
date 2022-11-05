import random
import re
import sys
import grpc
from concurrent import futures

from atuador import atuador_pb2
from atuador import atuador_pb2_grpc


atuador = atuador_pb2.HumidificadorResponse()
atuador.id = int(random.randrange(500))
atuador.nome = 'humidificador'
atuador.status = True


class ServerHumidificador(atuador_pb2_grpc.AtuadorGRPCServicer):
    def __init__(self) -> None:
        super().__init__()

    def ligarHumidificador(self, request, context):
            
            atuador.status = True

            to_txt = "80"

            with open("humidade.txt", 'w') as f:
                f.write(to_txt)
            f.close()
            return atuador

    def desligarHumidificador(self, request, context):
            
            atuador.status = False

            to_txt = "40"

            with open("humidade.txt", 'w') as f:
                f.write(to_txt)
            f.close()
            return atuador

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    atuador_pb2_grpc.add_AtuadorGRPCServicer_to_server(ServerHumidificador(), server)
    server.add_insecure_port("localhost:50053")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    
    
    try:
        print("Iniciando servidor Humidificador.")
        serve()
    except:
        print("Encerrando o servidor!")
        sys.exit(0)