from http import client
from rdt import*
from collections import namedtuple
from rdt import rdt_connection
'''
serverPort = 6000
serverIP = '' #localhost


while True:

    msg = server.receive()
    print(msg)


    print(f'Message received {rcvMsg}')
'''


options = """""""""
Digite uma das opções a seguir(o número ou por extenso)
1 - cardapio
2 - pedido
3 - conta individual
4 - nao fecho com robo, chame seu gerente
5 - nada nao, tava so testando
6 - conta da mesa
"""""""""

menu = """"
1 - Sassissinha : $10,00
2 - Acaraje : $15,50
3 - Casquinha de Siri : $13,00
4 - Torresmo: $10,00
5 - cudecurioso: $50,00
6 - Bolo de rolo: $5,00
"""

Products = {
    'Sassissinha': 10, 
    'Bolo de rolo': 10,
    'Acaraje':15,
    'Sassissinha': 10,
    'Cudecurioso': 50,
    'Torresmo':10
}

server = rdt_connection(6000, type='server')

table = []
ClientData = namedtuple('ClientData','id mesa conta_individual socket pedidos') 

sample_msg = "mensagem de resposta"

requests = []

def clientLogin(client_addr):
    msg = 'Digite sua mesa'
    server.rdt_send(msg, client_addr)
    
    client_addr2 = 'banana'
    
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            # TODO handle diferent clients messages
            #requests.append([pkt, client_addr2])
            continue
        elif not pkt['data'].isdigit():
            server.rdt_send('numero de mesa invalido', client_addr) 
        
    tableClient = pkt['data']
    msg = 'Digite seu nome'

    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])
        
    name = pkt['data']
    newClient = ClientData(id= name, mesa= tableClient, conta_individual= 0, socket=client_addr, pedidos=[])
    table.append(newClient)

    print('novo cliente cadastrado', newClient)

def isOption(option):
    if(option in range(1,7) or option == 'um' 
        or option == 'dois' or option == 'tres' 
        or option == 'quatro' or option == 'cinco' or option == 'seis'):
        return True
    
    return False
def handleMenu(client_addr):
    server.rdt_send(menu, client_addr)
    
    client_addr2 = 'abacate'
    option = None
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])

    handleOptions(option,client_addr)

def handleOrder(client_addr):
    msg = 'Digite qual o primeiro item que gostaria (número ou por extenso)'
    server.rdt_send(msg, client_addr)
    
    client_addr2 = 'abacate'
    option = None
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])
       
    
    handleOptions(option,client_addr)


def handleOptions(option, client_addr):
    print("testando")

    if option == '1'or option =='cardapio':
        handleMenu(client_addr)
        print('test')
    elif option == '2' or option =='pedir':
        print('test')
    elif option == '3' or option =='conta individual':
        print('test')
    elif option == '4' or option =='nao fecho com robo,chame seu gerente':
        print('test')
    elif option == '5' or option =='nada nao, tava so testando':
        print('test')
    elif option == '6' or option =='conta da mesa':
        print('test')
    else:
        print('escolher opcao válida')

def giveOptions(client_addr):
    server.rdt_send(options, client_addr)
    
    client_addr2 = 'abacate'
    option = None
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])
        elif isOption(pkt['data']):
            option = pkt['data']
        
    option = pkt['data']
    handleOptions(option, client_addr)
    
    
    
'''
def tablecount(client_addr,tableNumber):
    
    msg = []
    for client in table:
        if(client.mesa == tableNumber):
            
    ClientData = namedtuple('ClientData','id mesa conta_individual socket pedidos') 
    
    server.rdt_send(msg, client_addr)
    
    client_addr2 = 'banana'
    
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            # TODO handle diferent clients messages
            #requests.append([pkt, client_addr2])
            continue
        elif not pkt['data'].isdigit():
            server.rdt_send('numero de mesa invalido', client_addr) 
        
    tableClient = pkt['data']
    msg = 'Digite seu nome'
'''




while True:
    try:
        pkt, addr = server.rdt_rcv(type='receiver')
        print(pkt)

        if pkt['data'] == 'chefia':
            print('entrou chefia')
            clientLogin(addr)
            giveOptions(addr)
        elif pkt['data'] == 'opcao':
            # responde as opcoes do cliente
            print('continua bro')
        else:
            continue
    except Exception as err:
       print('err=', err)