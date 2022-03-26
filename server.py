import socket

serverPorta = 6000
serverIP = '' #localhost

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

serverID = (serverIP,serverPorta)

serverSocket.bind(serverID)

while True:

    recveivedMessageBytes,clientAdress = serverSocket.recvfrom(248)

    recveivedMessage = recveivedMessageBytes.decode()

    print("mensagem recebida:")
    print(recveivedMessage)
