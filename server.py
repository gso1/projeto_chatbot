from rdt import*

server = rdtConnection('localhost',6000,'server')

while True:

    msg = server.receive()
    print(msg)


