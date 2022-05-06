from rdt import rdt_connection
from collections import namedtuple
import time
'''
serverPort = 6000
serverIP = 'localhost'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverID = (serverIP, serverPort)

message = input("Type a message:")

clientSocket.sendto(message.encode(), serverID)
'''


client = rdt_connection(6000)
'''
<hora><nome_usuario>: <mensagem>  
onde:
<nome_usuario>: nome do usuário ou CINtofome
<mensagem>: mensagem recebida ou enviada
<hora>: hora da mensagem recebida, de acordo com o horário do servidor
'''
userName ='cliente'

state = 0

while True:
    try:
        if state%2 == 0:
            msg = input(f'<{time.localtime().tm_hour}:{time.localtime().tm_min} {userName}> :')
            print('antes')
            client.rdt_send(msg)
            
    
            state = state + 1
        if state%2 == 1:
             pkt, address = client.rdt_rcv(type='receiver')
             msg = pkt['data']
             print(f'<{time.localtime().tm_hour}:{time.localtime().tm_min} Cintofome> :{msg}')
             if msg == 'É pra já!':
                 continue
             state = state +1

    except KeyboardInterrupt:
        client.close_connection()
        break