from threading import Thread

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
            response = self.exec_command(args)
            self.connection.sendall(response.encode())
