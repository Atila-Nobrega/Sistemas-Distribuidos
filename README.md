# Sistemas-Distribuidos
## Professor:
* Paulo Antônio Leal Rêgo

## Equipe:
* Átila Nóbrega Maia Aires - 473754
* Tácio Soares Aguiar - 485214
* Luan Ícaro Ferreira Santos - 415170

## Slide Show:
[apresentacao.pdf](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/files/9710698/apresentacao.pdf)

# Trabalho 1:
## Task 1:
### Calculadora
A calculadora foi implementada em python utilizando protocolo UDP para comunicação server-client. Essa calculadora aceita as 4 operações básicas de soma, subtração, multiplicação e divisão.

O protocolo utilizado segue o padrão, em que, o client manda uma string para o servidor, que recebe e separa a string em 3 partes, transformando em float.  

Então resolve as operações de acordo com o símbolo que permanece em string.

As mensagens são enviadas e recebidas como string codificadas em ASCII, tanto no client quanto no server.

### Exemplo:
<details>
  <summary>Show:</summary>
  
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/calcexemplo.png?raw=true)
</details>

## Task 2:
### Chat Room:
O Chat Room foi implementado em python utilizando protocolo TCP para comunicação server-client. O Servidor do Chat funciona como uma sala de bate papo, onde os usuários podem se conectar utilizando o comando /entrar no client e inserindo o seu endereço.

Usuários conectados podem digitar mensagens que serão enviadas ao servidor e redirecionadas a todos os outros usuários conectados. Possuem também os comandos /usuarios para ver quem está conectado e /sair para se desconectar.

O Servidor possui threads responsáveis pelo envio e recebimento das mensagens e comandos. Ele também notifica os usuários quando uma nova conexão é feita ou desfeita.

As mensagens são enviadas e recebidas como string codificadas em ASCII, tanto no client quanto no server.
### Exemplo:
<details>
  <summary>Show:</summary>
  
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/codexemplo2.png?raw=true)
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/new1.png?raw=true)
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/new2.png?raw=true)
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/new3.png?raw=true)
</details>


## Task 3:
### Ambiente IoT:
Aplicação desktop em python usando a interface nativa python Tkinter, ela realiza uma comunicação em grupos de dispositivos com multicast e um servidor TCP. Usa Protocol Buffers para serialização dos dados estruturados de cada Device, ela é necessária para serializar a mensagem em um byte de string e enviar as mensagens entre clientes e servidor.

Usa threads para adicionar novos dispositivos que enviam e recebem mensagens, estes dispositivos que podem ser sensores, atuadores ou ambos. Os sensores são responsáveis por enviar valores, que seriam supostas medições e podem ser remotamente desconectados, já os atuadores recebem comandos para iniciar, deligar e desconectar.

O servidor tem 4 funções principais rodando em thread, uma para iniciar o multicast, outra para conectar os dispostivos, outra para receber as mensagens periodicamente e, por fim, a última trata de envia os comandos para os dispositvos.

O client tem 3 funções principais, uma para criar o objeto dispositivo, e outras duas para enviar e receber mensagens, onde ambas rodam em threads.

A troca de mensagens é feita por uma string de bytes.
### Exemplo:
<details>
  <summary>Show:</summary>
  
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/new4.png?raw=true)
  
  
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/new5.png?raw=true)
  
  
  ![alt text](https://github.com/Atila-Nobrega/Sistemas-Distribuidos/blob/main/assets/new6.png?raw=true)
</details>
