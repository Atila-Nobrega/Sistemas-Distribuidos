from fastapi import FastAPI
from pydantic import BaseModel
import socket
from time import sleep
from fastapi.middleware.cors import CORSMiddleware


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

while(True):
    try:
        client.connect(('127.0.0.1',2233))
        break
    except:
        print("Home assistance não encontrado... Verifique a conexão.")
        sleep(5)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Command(BaseModel):
    data: str

@app.post("/dispositivos")
async def create_item(command: Command):

    client.send(bytes(command.data,encoding="utf-8"))
    mensagem = client.recv(2048).decode("utf-8")

    return mensagem