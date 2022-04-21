import socket

from rdt import rdt_connection
'''
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
'''

server = rdt_connection(6000, type='server')
while True:
    try:
        pkt, _ = server.rdt_rcv(type='receiver')
        print(pkt)
    except KeyboardInterrupt:
        server.close_connection()
        break