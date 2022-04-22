import socket

from rdt import rdt_connection

'''
serverPort = 6000
serverIP = 'localhost'

clientSocket.sendto(message.encode(), serverID)
clientSocket.close() 
clientSocket.close()
'''

client = rdt_connection(6000)

while True:
    try:
        msg = input('Type message: ')
        client.rdt_send(msg)
    except KeyboardInterrupt:
        client.close_connection()
        break