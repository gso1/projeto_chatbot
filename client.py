import socket

serverPort = 6000
serverIP = 'localhost'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverID = (serverIP, serverPort)

message = input("Type a message:")

clientSocket.sendto(message.encode(), serverID)

clientSocket.close()