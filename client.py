from rdt import rdt_connection

'''
serverPort = 6000
serverIP = 'localhost'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverID = (serverIP, serverPort)

message = input("Type a message:")

clientSocket.sendto(message.encode(), serverID)
'''


client = rdt_connection(6000)

while True:
    try:
        msg = input('Type message: ')
        client.rdt_send(msg)
    except KeyboardInterrupt:
        client.close_connection()
        break