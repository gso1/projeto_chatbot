from rdt import rdt_connection
from collections import namedtuple
import time

# inicia o cliente
client = rdt_connection(6000)
'''
<hora><nome_usuario>: <mensagem>  
onde:
<nome_usuario>: nome do usuário ou CINtofome
<mensagem>: mensagem recebida ou enviada
<hora>: hora da mensagem recebida, de acordo com o horário do servidor
'''

# define o nome inicial de todo usuario
userName ='cliente'

# flag para receber o nome de um usuario
nameFlag = False

# estado em que se encontra o cliente
state = 0

# flag para termino do cliente
end = False

# loop principal
while True:

    '''
        Dependendo do estado nos vamos estar enviando ou esperando uma resposta do servidor.
        quando state = 0, estamos enviando, caso contrario estamos esperando.
    '''
    try:
        if state == 0:
            #send
            msg = input(f'<{time.localtime().tm_hour}:{time.localtime().tm_min} {userName}> :')
            client.rdt_send(msg)
            if nameFlag:
                userName = msg
                nameFlag = False
            
            state = 1

        if state == 1:
            #rcv
            print('Esperando resposta do servidor...')
            pkt, address, _ = client.rdt_rcv(type='receiver')
            
            if pkt['data'] == 'Digite seu nome':
                nameFlag = True
         
            msg = pkt['data']
            print(f'<{time.localtime().tm_hour}:{time.localtime().tm_min} Cintofome> :{msg}')
            state = 0
            if pkt['data'] == 'Volte Sempre ^^':
                raise "End of client"

    except KeyboardInterrupt:
        client.close_connection()
        break
    except Exception as err:
        client.close_connection()
        break
        
client.close_connection()