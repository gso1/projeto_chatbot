import socket

class rdt_connection:
    
    seq_num = 1

    def __init__(self, port, ip='localhost', type='client', buffer_size=248):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (ip, port)
        self.buffer_size = buffer_size
        if type == 'server':
            print(f'Server listening on port {port}')
            self.sock.bind(self.address)
    
    def udt_send(self, msg):
        return self.sock.sendto(msg, self.address)
    
    def udt_rcv(self):
        return self.sock.recvfrom(self.buffer_size)

    def rdt_send(self, msg):
        pkt = self.make_pkt(self.seq_num, msg)
        self.seq_num += 1
        self.udt_send(pkt.encode())

        #agora espera por ack
        ack = False
        while not self.ack:
            pkt, _ = self.rdt_rcv()
            
    
    def rdt_rcv(self):
        
        bytes, sender_addr = self.udt_rcv(248)
        pkt = eval(bytes.decode())
        return pkt, sender_addr

    def make_pkt(self, seq_num, msg):
        return str({'seq_num': seq_num, 'sum': self.checksum(msg) ,'data': msg})

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