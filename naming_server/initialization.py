import socket
from time import sleep

from threading import Thread



class ProbeListener(Thread):

    def __init__(self, socket):
        super().__init__(daemon=True)
        self.socket = socket

    def run(self):

        while True:
            data, addr = self.socket.recvfrom(1024)
            print(f"recieved message: {data} from address {addr}")
            if data == b'hello':
                self.socket.sendto(b'connect to me!', addr)
            

class StorageManager(Thread):

    def __init__(self, socket):
        
        super().__init__(daemon=True)
        self.socket = socket
        self.servers = {}

        
    def run(self):

        while True:
            conn, addr = self.socket.accept()
            print(f'{addr} connected')

            self.servers[addr] = conn

            
            
            
        
        
