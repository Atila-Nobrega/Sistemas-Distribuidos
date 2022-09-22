import socket

serverAddressPort   = ("127.0.0.1", 20001)

# Create a UDP socket at client side
client = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

print("Exemplo :4 + 5")
print("Digite 'fim' para encerrar o cliente e servidor"); 
# Send to server using created UDP socket
while True:
    # here we get the input from the user
    inp = input("Insira o calculo: ")
    # If user wants to terminate
    # the server connection he can type fim
    if inp == "fim":
        print("Encerrando o cliente e servidor")
        client.sendto(inp.encode(), serverAddressPort)
        break
    # Here we send the user input
    # to server socket by send Method
    client.sendto(inp.encode(), serverAddressPort)
 
    # Here we received output from the server socket
    answer = client.recv(1024)
    print("Resposta: "+answer.decode())
    print("Escreva fim para finalizar")

client.close()
print("Cliente encerrado!")