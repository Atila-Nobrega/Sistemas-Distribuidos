import re
import sys
import grpc
from concurrent import futures

from atuador import atuador_pb2
from atuador import atuador_pb2_grpc




    

def ArCondicionado():
        with grpc.insecure_channel('localhost:50051') as channel:
            stub = atuador_pb2_grpc.AtuadorGRPCStub(channel)

            print("1. para ligar ar condicionado")
            print("2. para desligar ar condicionado")
            print("3. para aumentar a temperatura")
            print("4. para diminuir a temperatura")
            
            grpc_call = input('Digite um comando: ')
            if (grpc_call == '1'):
                ar_request = atuador_pb2.ArCondicionadoRequest()
                ar_reply = stub.ligarArCondicionado(ar_request)
                print(ar_reply)
            
            if (grpc_call == '2'):
                ar_request = atuador_pb2.ArCondicionadoRequest()
                ar_reply = stub.desligarArCondicionado(ar_request)
                print(ar_reply)
            
            if (grpc_call == '3'):
                ar_request = atuador_pb2.ArCondicionadoRequest()
                ar_reply = stub.aumentarTemperatura(ar_request)
                print(ar_reply)
            
            if (grpc_call == '4'):
                ar_request = atuador_pb2.ArCondicionadoRequest()
                ar_reply = stub.diminuirTemperatura(ar_request)
                print(ar_reply)

def Lampada():
        with grpc.insecure_channel('localhost:50052') as channel:
            stub = atuador_pb2_grpc.AtuadorGRPCStub(channel)
            
            print("1. para ligar a Lampada")
            print("2. para desligar a Lampada")
            grpc_call = input('Digite um comando: ')

            if (grpc_call == '1'):
                lampada_request = atuador_pb2.LampadaRequest()
                lampada_reply = stub.ligarLampada(lampada_request)
                print(lampada_reply)
            
            if (grpc_call == '2'):
                lampada_request = atuador_pb2.LampadaRequest()
                lampada_reply = stub.desligarLampada(lampada_request)
                print(lampada_reply)
            
            
           
def Humidificador():
        with grpc.insecure_channel('localhost:50053') as channel:
            stub = atuador_pb2_grpc.AtuadorGRPCStub(channel)
            
            print("1. para ligar o humidificador")
            print("2. para desligar o humidificador")
            grpc_call = input('Digite o humidificador: ')
            if (grpc_call == '1'):
                humidificador_request = atuador_pb2.HumidificadorRequest()
                humidificador_reply = stub.ligarHumidificador(humidificador_request)
                print(humidificador_reply)
            
            if (grpc_call == '2'):
                humidificador_request = atuador_pb2.HumidificadorRequest()
                humidificador_reply = stub.desligarHumidificador(humidificador_request)
                print(humidificador_reply)
           


if __name__ == "__main__":
    

    try:
        while(True):    
            print("1. Acessar ar condicionado")
            print("2. Acessar lampada")
            print("3. Acessar umidificador")
            rpc_call = input("Qual dispositivo você deseja acessar?")

            if(rpc_call == '1'):
                ArCondicionado()

            if(rpc_call == '2'):
                Lampada()


            if(rpc_call == '3'):
                Humidificador()
    except:
        print("Encerrando o home assistance!")
        sys.exit(0)