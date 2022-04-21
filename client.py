import socket
import json 
from rdt import rdtConnection

class data:

    def __init__(self,seq,checksum,message,timeout):
        self.seq = seq
        self.checksum = checksum
        self.message = message
        self.timeout = timeout

    def to_json(self):
        '''
        convert the instance of this class to json
        '''
        return json.dumps(self, indent = 4, default=lambda o: o.__dict__)

client = rdtConnection(ip='localhost', port=6000)

while True:
    msg = input('Type a message ')
    client.send(msg)



