from rdt import*


from rdt import rdt_connection
'''
serverPort = 6000
serverIP = '' #localhost


while True:

    msg = server.receive()
    print(msg)


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

