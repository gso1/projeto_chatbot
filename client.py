from rdt import rdt_connection
from collections import namedtuple
import time

client = rdt_connection(6000)
'''
<hora><nome_usuario>: <mensagem>  
onde:
<nome_usuario>: nome do usuário ou CINtofome
<mensagem>: mensagem recebida ou enviada
<hora>: hora da mensagem recebida, de acordo com o horário do servidor
'''
userName ='cliente'
nameFlag = False
state = 0
end = False

while True:
    try:
        if state%2 == 0:
            
            msg = input(f'<{time.localtime().tm_hour}:{time.localtime().tm_min} {userName}> :')
            client.rdt_send(msg)

            if nameFlag:
                userName = msg
                nameFlag = False
            
            if msg.lower() == 'levantar':
                end = True

            state = state + 1

        if state%2 == 1:
            
            pkt, address, _ = client.rdt_rcv(type='receiver')
            
            if pkt['data'] == 'Digite seu nome':
                nameFlag = True

            if end:
                raise "End of client"
            msg = pkt['data']
            print(f'<{time.localtime().tm_hour}:{time.localtime().tm_min} Cintofome> :{msg}')
            state = state +1

    except KeyboardInterrupt:
        client.close_connection()
        break
    except Exception as err:
        client.close_connection()
        break