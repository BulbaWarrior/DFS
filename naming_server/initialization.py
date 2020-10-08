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
        self.servers = []

        
    def run(self):

        while True:
            conn, addr = self.socket.accept()
            print(f'{addr} connected')

            self.servers.append(conn)


class ClientListener(Thread):

    def __init__(self, connection,  storage_manager):
        super().__init__(daemon=True)
        self.storage_manager = storage_manager
        self.connection = connection

        
    def parse_data(self, data):
        s = data.decode().split('\n')[0]
        return s.split(' ')

    def exec_command(self, args):
        #TODO
        return ' '.join(args) + '\n'


    def run(self):

        while True:

            data = self.connection.recv(1024)
            if not data: # client ended communication
                self.connection.close()
                break

            
            args = self.parse_data(data)
            answer = self.exec_command(args)
            self.connection.sendall(answer.encode())
            
            
            
        
        
