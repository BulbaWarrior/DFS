from threading import Thread
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('infile', nargs='?')
parser.add_argument('outfile', nargs='?')


class ServerListener(Thread):

    def create(self, args):
        fd = open(args.infile, 'w')
        fd.close()
        print('created ' + args.infile)

    def delete(self, args):
        os.remove(args.infile)

    def __init__(self, connection):
        super().__init__(daemon=True)
        self.connection = connection

        commands = [self.create, self.delete]
        self.commands = {func.__name__: func for func in commands}

    def run(self):
        while True:
            data = self.connection.recv(1024)
            if not data:
                print('warning! connection to naming server lost!')
                self.connection.close()
                break

            print(f'recieved data: {data}')

            args = parser.parse_args(args=data.decode().split(' '))
            command = args.command
            if command not in self.commands:
                print(f'unrecognized command {command}')

            self.commands[command](args)


class ClientListener(Thread):

    def pull(self, args):
        pass

    def push(self, args):
        pass

    def info(self, args):
        pass

    def __init__(self, connection):
        super().__init__(daemon=True)
        self.connection = connection
        commands = [self.push, self.pull, self.info]
        self.commands = {func.__name__: func for func in commands}

    def run(self):

            data = self.connection.recv(1024)

            if not data:
                self.connection.close()
                return

            args = data.decode().split()
            args = parser.parse_args(args=args)

            command = args.command
            self.commands[command](args)
            self.connection.close()
            return
                
