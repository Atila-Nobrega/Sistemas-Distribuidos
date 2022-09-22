import socket 

localIP = "127.0.0.1"
localPort = 20001
bufferSize = 1024 

msgFromServer = "Sucesso conexao com client"
bytesToSend = str.encode(msgFromServer)

# Create a datagram socket
server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Bind to address and ip
server.bind((localIP, localPort))
print("UDP server up and listening")

# Listen for incoming datagrams
while True:
    data = server.recvfrom(bufferSize)
    message = data[0]
    address = data[1]
    msg = message.decode()
    if msg == 'fim':
        print("Fim da conexão!")
        break
 
    print("Equação recebida")
    resultado = 0
    operacao_list = msg.split()
    oprnd1 = operacao_list[0]
    operacao = operacao_list[1]
    oprnd2 = operacao_list[2]
 
    # here we change str to int converstion
    num1 = int(oprnd1)
    num2 = int(oprnd2)
    # Here we are perform  basic arithmetic operacao
    if operacao == "+":
        resultado = num1 + num2
    elif operacao == "-": 
        resultado = num1 - num2
    elif operacao == "/":
        resultado = num1 / num2
    elif operacao == "*":
        resultado = num1 * num2
 
    print("Resultado enviado")
   
    output = str(resultado)
    server.sendto(output.encode(), address)