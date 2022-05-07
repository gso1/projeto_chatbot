from gettext import find
from http import client
from rdt import*
from collections import namedtuple
from rdt import rdt_connection

class ClientData:

    def __init__(self,id, mesa, socket):

        self.id = id
        self.mesa = mesa
        self.conta_individual = 0
        self.socket = socket
        self.pedidos = []

    def printData(self):
        
        print(f'id : {self.id}')
        print(f'mesa : {self.mesa}')
        print(f'conta_individual : {self.conta_individual}')
        print(f'socket : {self.socket}')
        print(f'pedidos : {self.pedidos}')
       

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
5 - Cudecurioso: $50,00
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
    server.rdt_send(msg, client_addr)
    #client_addr2 = 'banana'
    ok = False
    while not ok:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])
        
    name = pkt['data']
    newClient = ClientData(id= name, mesa= tableClient, socket=client_addr)
    table.append(newClient)

    print('novo cliente cadastrado', newClient)
    

def isOption(option):
    if(option in ['1','2','3','4','5','6'] or option == 'cardapio'
        or option == 'pedir' or option == 'conta individual' 
        or option == 'conta da mesa' or option == 'pagar' or option == 'levantar'):
        return True
    
    return False

def isPlate(plate):
    if(plate in Products.keys()):
        return True
    
    return False

def handleMenu(client_addr):
    server.rdt_send(menu, client_addr)
    

def finishOrder(client_addr):
    msg = 'É pra já!'
    server.rdt_send(msg, client_addr)
   


def newOrder(client_addr):
    msg = 'Gostaria de pedir mais algum item?(sim ou nao)'
    server.rdt_send(msg, client_addr)

    print('dentro new order')
    client_addr2 = 'abacate'
    option = None
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        option = pkt['data']
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])
        elif option == 'sim':
            print(isPlate(pkt['data']))
            option = pkt['data']
            handleOrder(client_addr)
        elif option == 'nao':
            print(isPlate(pkt['data']))
            option = pkt['data']
            finishOrder(client_addr)
        else:
            msg = "Digite apenas 'sim' ou 'nao' " 
            handleError(msg,client_addr2)
            client_addr2 = 'abacate'

def addPlate(client_addr,plate):
    print('no add plate')
    for person in table:
        if person.socket == client_addr:
            print('antes append')
            person.pedidos.append([plate,Products[plate]])
            print('antes att conta')
            person.conta_individual = person.conta_individual + Products[plate]
            print('printar perso')
            person.printData()
    

def handleOrder(client_addr):
    msg = 'Digite qual o primeiro item que gostaria (número ou por extenso)'
    server.rdt_send(msg, client_addr)

    client_addr2 = 'abacate'
    plate = None
    while client_addr2 != client_addr:
        pkt, client_addr2 = server.rdt_rcv(type='receiver')
        if client_addr2 != client_addr:
            requests.append([pkt, client_addr2])
        elif isPlate(pkt['data']):
            print(isPlate(pkt['data']))
            plate = pkt['data']
        else:
            msg = "Digite apenas pratos que existam no menu"
            handleError(msg,client_addr2)
            client_addr2 = 'abacate'

    addPlate(client_addr,plate)
    
    newOrder(client_addr)
    
def clientInfo(client_addr):
    print('countInfo')
    msg = 'Default'
    for person in table:
        person = findClient(client_addr)
        print('achou')
        msg = '\n|' + person.id +'|\n'
        print('antes for pedido')
        for pedido in person.pedidos:
            print(person.pedidos)
            msg = msg + pedido[0] + ' =>R$ ' + str(pedido[1]) + '\n'
            msg = msg + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n'
        msg = msg + 'Total = R$' + str(person.conta_individual) + '\n'
        msg = msg + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n\n'
    return msg

def individualCount(client_addr):
    print('individualCount')
    msg = 'Default'
    msg = clientInfo(client_addr)
    server.rdt_send(msg, client_addr)
    


def findClient(client_addr):
    for person in table:
        if(person.socket == client_addr):
            return person
    return None

def tableCount(client_addr):
    print('tableCount')
    msg = 'Default'
    person = findClient(client_addr)
    numberTable = person.mesa
    total = 0

    for person in table:
        if person.mesa == numberTable:
            msg = msg + clientInfo(person.socket)
            total = total + person.conta_individual

    msg = msg + 'Total da mesa = R$' + str(total) + ',00\n'
    msg = msg + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n\n'
    
    server.rdt_send(msg, client_addr)
  

def totalTable(client_addr):
    person = findClient(client_addr)
    numberTable = person.mesa
    total = 0
    for person in table:
        if person.mesa == numberTable:
            
            total = total + person.conta_individual
    return total

    
def pay_account(client_addr):
    client = findClient(client_addr)
    clientBill = client.conta_individual
    tableBill = totalTable(client_addr)

    msg = f'Sua conta foi R$ {clientBill} e a da mesa R$ {tableBill}. Digite o valor a ser pago'
    server.rdt_send(msg, client_addr)
    snd_addr = None
    payment = None
    print('antes while')
    while snd_addr != client_addr:
        
        pkt, snd_addr = server.rdt_rcv(type = 'receiver')
        print(pkt['data'])
        print(pkt['data'].isdigit())
        if not pkt['data'].isdigit():
            msg = 'Escreva apenas digitos'
            handleError(msg,client_addr)
            snd_addr = 'banana'
            continue
        else:
            payment = float(pkt['data'])
    
    print('pos while')
    if payment < clientBill or payment > tableBill:
        pay_account(client_addr)
    elif payment == clientBill :
        print('equal')
        clientBill -= payment
        client.conta_individual = 0
    elif payment <= tableBill:
        client.conta_individual = 0
        rest = payment - clientBill
        dividePayment(rest, client_addr)

    msg = 'Você pagou sua conta, obrigado!'
    print(client.conta_individual)
    server.rdt_send(msg, client_addr)
    print('pos send')

        
        
def dividePayment(rest, client):
    mesa = client.mesa

    countValid = 0
    count = 0
    
    for person in table:
        if person.mesa == mesa and person.conta_individual:
            count += 1
    
    if not count:
        return False

    individualPayment = rest/count

    for person in table:
        if person.mesa == mesa and person.conta_individual:
            person.conta_individual = max(0, person.conta_individual - rest)
    
    return True
            
def clientRemove(client_addr):
    
    person = findClient(client_addr)

    print('clientremove antes if')
    if person.conta_individual:
        msg = 'Você ainda não pagou sua conta'
        handleError(msg ,client_addr)
        return
    
    person = findClient(client_addr)
    index = table.index(person)
    table.pop(index)
    msg = 'Volte Sempre ^^'
    server.rdt_send(msg, client_addr)
    
    
def handleOptions(option,client_addr):
    print("no handle options")

    if option == 'chefia':
        print('entrou chefia')
        clientLogin(addr)
        giveOptions(addr)
    elif option == '1'or option =='cardapio':
        handleMenu(client_addr)
        print('test 1')
    elif option == '2' or option =='pedir':
        handleOrder(client_addr)
        print('test 2')
    elif option == '3' or option =='conta individual':
        individualCount(client_addr)
        print('test 3')
    elif option == '4' or option =='nao fecho com robo,chame seu gerente':
        print('test 4')
    elif option == '5' or option =='nada nao, tava so testando':
        print('test 5')
    elif option == '6' or option =='conta da mesa':
        tableCount(client_addr)
        print('test 6')
    elif option == 'levantar':
        clientRemove(client_addr)
        print('test 7')
    elif option == 'pagar':
        pay_account(client_addr)
        print('test 8')
    else:
        print(option)
        print('escolher opcao válida')

def handleError(msg, client_addr):
    msgDefault = 'Ocorreu um erro:'
    msg = msgDefault + msg
    server.rdt_send(msg, client_addr)


def giveOptions(client_addr):

    server.rdt_send(options, client_addr)
    
    
    
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


def foo(pkt, cliente_end):
    server.rdt_send('opa', cliente_end)
    pkt, end, valid = server.rdt_rcv(cliente_end, type='receiver')
    while not valid: 
        pkt, end, valid = server.rdt_rcv(cliente_end, type='receiver')

    server.rdt_send('ok', cliente_end)

if __name__ == '__main__':
    while True:
        try:
            pkt, addr, _ = server.rdt_rcv(type='receiver')
            print(pkt)
            foo(pkt, addr)
            '''if pkt['data'] == 'chefia':
                flag = 0
                for person in table:
                    if person.socket == addr:
                        msg = 'Usuário já cadastrado'
                        handleError(msg,addr)
                        flag = 1
                if flag == 1:
                    continue

                print('entrou chefia')
                clientLogin(addr)
                giveOptions(addr)

            elif isOption(pkt['data']):
                # responde as opcoes do cliente
                option = pkt['data']
                handleOptions(option,addr)
            else :
                msg = 'Opcao inválida'
                handleError(msg,addr)
                print('continua bro')'''
            
        except Exception as err:
            print('err=', err)