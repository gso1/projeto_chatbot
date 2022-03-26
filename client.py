import socket

serverPorta = 6000
serverIP = '192.168.15.160'

clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

serverID = (serverIP,serverPorta)


message = input("inputa ai:")

clientSocket.sendto(message.encode(),serverID)

clientSocket.close()