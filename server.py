from gettext import find
from http import client
from rdt import*
from collections import namedtuple
from rdt import rdt_connection

# classe que armazena os dados do cliente
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


# strings e dicionarios auxiliares

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
5 - Rabada: $50,00
6 - Bolo de rolo: $5,00
"""

Products = {
    'Sassissinha': 10.0, 
    'Acaraje':15.5,
    'Casquinha de Siri': 13.,
    'Torresmo': 10.,
    'Rabada': 50.,
    'Bolo de rolo': 10.0
}

ProductsNum = {
    '1': 10. ,
    '2': 15.5,
    '3': 13.,
    '4': 10.,
    '5': 50.,
    '6': 10.
}


# inicia o servidor
server = rdt_connection(6000, type='server')

# representa uma matriz de clientes no restaurante
table = []
 

sample_msg = "mensagem de resposta"

# faz o login do cliente
def clientLogin(client_addr):
    msg = 'Digite sua mesa'
    server.rdt_send(msg, client_addr)
    
    valid = False
    pkt, _, valid = server.rdt_rcv(type='receiver',addr=client_addr)
    
    # espera por uma resposta do cliente para seguir o processo
    while not valid:
        if valid and not pkt['data'].isdigit():
            server.rdt_send('numero de mesa invalido', client_addr) 
        pkt, _, valid = server.rdt_rcv(type='receiver', addr=client_addr)
        
    tableClient = pkt['data']

    msg = 'Digite seu nome'
    server.rdt_send(msg, client_addr)
    valid = False

    while not valid:
        pkt, _, valid = server.rdt_rcv(type='receiver', addr=client_addr)
        
    name = pkt['data']
    newClient = ClientData(id=name, mesa=tableClient, socket=client_addr)
    table.append(newClient)

    print('novo cliente cadastrado', newClient)
    

# checa se eh uma opcao valida
def isOption(option):
    if (option in ['1','2','3','6'] or option == 'cardapio'
        or option == 'pedir' or option == 'conta individual' 
        or option == 'conta da mesa' or option == 'pagar' or option == 'levantar'):
        return True
    
    return False

# checa se eh um pedido valido
def isPlate(plate):
    if (plate in Products.keys())or (plate in ['1','2','3','4','5','6']):
        return True
    return False

# envia o menu pro usuario
def handleMenu(client_addr):
    server.rdt_send(menu, client_addr)
    
# Finaliza o pedido do usuario
def finishOrder(client_addr):
    msg = 'É pra já!'
    server.rdt_send(msg, client_addr)
   

# faz um novo pedido
def newOrder(client_addr):
    msg = 'Gostaria de pedir mais algum item?(sim ou nao)'
    server.rdt_send(msg, client_addr)

    option = None
    valid = False
    while not valid:
        pkt, _, valid = server.rdt_rcv(type='receiver', addr=client_addr)
        
        if not valid:
            continue

        option = pkt['data']
        if option == 'sim':
            handleOrder(client_addr)
        elif option == 'nao':
            finishOrder(client_addr)
        else:
            msg = "Digite apenas 'sim' ou 'nao' " 
            handleError(msg,client_addr)
            valid = False
           
# adciona um prato no cliente
def addPlate(client_addr,plate):
    print('no add plate')
    if plate in ['1','2','3','4','5','6']:
        plate = int(plate)
        plate = list(Products.keys())[plate-1]

    for person in table:
        if person.socket == client_addr:
            print('antes append')
            person.pedidos.append([plate,Products[plate]])
            print('antes att conta')
            person.conta_individual = person.conta_individual + Products[plate]
            print('printar perso')
            person.printData()
    
# recebe o pedido do cliente
def handleOrder(client_addr):
    msg = 'Digite qual o item que gostaria (número ou por extenso)'
    server.rdt_send(msg, client_addr)

    plate = None
    valid = False

    while not valid:
        pkt, _, valid = server.rdt_rcv(type='receiver', addr=client_addr)
        if not valid:
            continue

        if isPlate(pkt['data']):
            print(isPlate(pkt['data']))
            plate = pkt['data']
        else:
            msg = "Digite apenas pratos que existam no menu"
            handleError(msg, client_addr)
            valid = False

    addPlate(client_addr,plate)
    
    newOrder(client_addr)
    
# Manda as informacoes do cliente
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

# Manda a conta individual do cliente
def individualCount(client_addr):
    print('individualCount')
    msg = 'Default'
    msg = clientInfo(client_addr)
    server.rdt_send(msg, client_addr)
    

# Procura por cliente
def findClient(client_addr):
    for person in table:
        if(person.socket == client_addr):
            return person
    return None

# Manda a conta da mesa
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

    msg = msg + 'Total da mesa = R$' + str(total) + '\n'
    msg = msg + '-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-\n\n'
    
    server.rdt_send(msg, client_addr)
  
# Cacula a conta total da mesa do cliente
def totalTable(client_addr):
    person = findClient(client_addr)
    numberTable = person.mesa
    total = 0
    for person in table:
        if person.mesa == numberTable:
            
            total = total + person.conta_individual
    return total

def check_float(potential_float):
    try:
        float(potential_float)
        return True
    except ValueError:
        return False

# Faz o pagamento da conta do cliente   
def pay_account(client_addr):
    client = findClient(client_addr)
    clientBill = client.conta_individual
    tableBill = totalTable(client_addr)

    msg = f'Sua conta foi R$ {clientBill} e a da mesa R$ {tableBill}. Digite o valor a ser pago'
    server.rdt_send(msg, client_addr)
    payment = None
    valid = False
    while not valid:
        
        pkt, _, valid = server.rdt_rcv(type = 'receiver', addr=client_addr)
        print(pkt['data'])
        print(pkt['data'].isdigit())
        
        if not valid:
            continue

        if not check_float(pkt['data']):
            msg = 'Escreva apenas digitos'
            handleError(msg,client_addr)
            valid = 'false'
        else:
            payment = float(pkt['data'])
    
            if payment < clientBill or payment > tableBill:
                valid = False
                msg = f'Sua conta foi R$ {clientBill} e a da mesa R$ {tableBill}. Digite o valor a ser pago'
                handleError(msg,client_addr)
            elif payment == clientBill :
                print('equal')
                clientBill -= payment
                client.conta_individual = 0
            elif payment <= tableBill:
                client.conta_individual = 0
                rest = payment - clientBill
                dividePayment(rest, client_addr)

    client.pedidos.clear()

    msg = 'Você pagou sua conta, obrigado!'
    print(client.conta_individual)
    server.rdt_send(msg, client_addr)
   

# divide o pagamento do cliente        
def dividePayment(rest, client_addr):
    client = findClient(client_addr)
    mesa = client.mesa

    count = 0
    
    for person in table:
        if person.mesa == mesa and person.conta_individual:
            count += 1
    
    if not count:
        return False

    individualPayment = rest/count

    for person in table:
        if person.mesa == mesa and person.conta_individual:
            person.conta_individual = max(0, person.conta_individual - individualPayment)
    
    return True

# remove o cliente    
def clientRemove(client_addr):
    
    person = findClient(client_addr)

    if person.conta_individual:
        msg = 'Você ainda não pagou sua conta'
        handleError(msg ,client_addr)
        return
    
    person = findClient(client_addr)
    index = table.index(person)
    table.pop(index)
    msg = 'Volte Sempre ^^'
    server.rdt_send(msg, client_addr)
    

# encaminha o cliente para a opcao desejada
def handleOptions(option, client_addr):
    print("no handle options")

    
    if option == '1'or option =='cardapio':
        handleMenu(client_addr)
    elif option == '2' or option =='pedir':
        handleOrder(client_addr)
    elif option == '3' or option =='conta individual':
        individualCount(client_addr)
    elif option == '6' or option =='conta da mesa':
        tableCount(client_addr)
    elif option == 'levantar':
        clientRemove(client_addr)
    elif option == 'pagar':
        pay_account(client_addr)
    else:
        print(option)
        print('escolher opcao válida')

def handleError(msg, client_addr):
    msgDefault = 'Ocorreu um erro:'
    msg = msgDefault + msg
    server.rdt_send(msg, client_addr)


def giveOptions(client_addr):
    server.rdt_send(options, client_addr)
    

if __name__ == '__main__':
    while True:
        try:
            pkt, addr, _ = server.rdt_rcv(type='receiver')
            print(pkt)
            if pkt['data'] == 'chefia':
                flag = 0
                for person in table:
                    if person.socket == addr:
                        msg = 'Usuário já cadastrado'
                        handleError(msg,addr)
                        flag = 1
                if flag == 1:
                    continue

                clientLogin(addr)
                giveOptions(addr)

            elif isOption(pkt['data']):
                # responde as opcoes do cliente
                option = pkt['data']
                handleOptions(option,addr)
            else :
                msg = 'Opcao invalida'
                handleError(msg, addr)
                print('continua bro')
            
        except Exception as err:
            print('main err=', err)