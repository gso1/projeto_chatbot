import socket

serverPort = 6000
serverIP = '' #localhost

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverID = (serverIP, serverPort)

serverSocket.bind(serverID)

print(f'Listenning on port {serverPort}')
while True:

    rcvMsgBytes, clientAdress = serverSocket.recvfrom(248)

    rcvMsg = rcvMsgBytes.decode()

    print(f'Message received {rcvMsg}')
