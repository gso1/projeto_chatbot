import socket
from random import random

class rdt_connection:

    def __init__(self, port, ip='localhost', type='client', buffer_size=248):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_addr = (ip, port)
        self.buffer_size = buffer_size
        self.type = type
        self.seq_num = 0
        if type == 'server':
            print(f'Server listening on port {port}')
            self.sock.bind(self.server_addr)
    
    def udt_send(self, msg, addr=None):
        if addr == None:
            addr = self.server_addr

        return self.sock.sendto(msg, addr)
    
    def udt_rcv(self):
        return self.sock.recvfrom(self.buffer_size)

    def rdt_send(self, msg):
        sum = self.checksum(msg.encode())
        pkt = self.make_pkt(msg, sum)
        pktsnd = pkt.encode()
        self.sock.settimeout(1)
        self.udt_send(pktsnd)

        ack = 0
        while not ack:
            try:
                pktrcv, _ = self.rdt_rcv()
                if pktrcv['sum'] != sum or pktrcv['ack'] != self.seq_num:
                    continue
            except socket.timeout as err:
                print('timeout error')
                self.udt_send(pktsnd)
                self.sock.settimeout(1)
            else:
                self.sock.settimeout(None)
                ack = 1
        self.seq_num = 1 - self.seq_num
                    
    def rdt_rcv(self, type='sender'):
        bytes, sender_addr = self.udt_rcv()
        pkt = eval(bytes.decode())
        isvalid = True
        # p = random()
        if type == 'receiver':
            sum = self.checksum(pkt['data'].encode())
            sndack = self.make_ack(sum, ack=self.seq_num)

            if self.corrupt(pkt) or self.seq_num != pkt['seq']:
                sndack['ack'] = pkt['seq']
                isvalid = False
            else:
                self.seq_num = 1 - self.seq_num
            
            self.udt_send(str(sndack).encode(), addr=sender_addr)
        
        return (pkt, sender_addr) if isvalid else (None, None)

    def make_pkt(self, msg, checksum, ack=1):
        return str({'seq': self.seq_num, 'sum': checksum, 'data': msg})

    def make_ack(self, checksum, ack=1):
        return {'ack': ack, 'sum': checksum}

    def corrupt(self, pkt):
        return pkt['sum'] != self.checksum(pkt['data'].encode())

    def checksum(self, data):
        #RFC 1071
        addr = 0 
        # Copute Internet Checksum for "count" bytes, begining at location "addr"
        Sum = 0
        count = len(data)
        while (count > 1):
            # inner loop
            Sum += data[addr] << 8 + data[addr+1]  # index do byte 
            addr += 2
            count -= 2

        # add left-over byte, if any
        if (count > 0):
            Sum += data[addr]

        # fold 32-bit Sum to 16 bits
        while (Sum>>16):
            Sum = (Sum & 0xffff) + (Sum >> 16)

        checksum = ~Sum
        return checksum

    def close_connection(self):
        print('Closing socket')
        self.sock.close()