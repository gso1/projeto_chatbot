import socket
import json
from types import new_class

from checksum import checksum

class rdtConnection:

    seqNumber = 0

    def __init__(self, ip: str, port: int, type: str = "client") -> socket.socket:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = (ip, port)
        self.type = type
        if type == "server":
            print(f'server listening on {port}')
            self.sock.bind(self.address)
            
    def send(self, pkt: dict[str,int]) -> int:
        return self.sock.sendto(pkt.encode(), self.address)

    def rdtSend(self, msg: str) ->None:
        self.sock.settimeout(1)
        sndpkt = self.make_pkt(msg)
        self.send(self, sndpkt)
        response = False
        while not response:
            try:
                rcvpkt = self.rdtReceive()
                self.sock.settimeout(None)
            except socket.timeout as err:
                print('timeout')
            
            if self.corrupt(rcvpkt, sndpkt) or self.isACK(rcvpkt, 1):
                print('ok')
                response = True
    
    def isCorrupt(self, rcvpkt, sndpkt):
        return rcvpkt['checkSum'] == sndpkt['checkSum']:

    def isACK(self, rcvpkt, ack):
        print("opa")
        
    def make_pkt(self, msg: str) -> dict[str,int]:
        checkSum = self.checkSum(msg)
        dic = {'ack': 0,'seq': self.seqNum,'checkSum': checkSum, 'msg' : msg}

        return dic

    def rdtReceive(self):
        rcvMsgBytes, serverAdress = self.sock.recvfrom(248)
        rcvMsg = rcvMsgBytes.decode()
       
       
        return self.receive(rcvMsg)
        
    def receive(self,rcvMsg:str) -> str:
        #sendACK
        return rcvMsg
    
    def sendAck(self):
        return self.seqNumber

    def checkSum(self, data: str) -> int:
        print("checa o checksum")

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


