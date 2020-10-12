from threading import Thread
import os
import argparse
import random


# single_commands = ['init', 'ls']
# unary_commands = ['create', 'read', 'rm', 'info', 'cd', 'rmdir']
# binary_commands = ['write', 'cp', 'mv']
# commands = [*single_commands, *unary_commands, *binary_commands]

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('infile', nargs='?')
parser.add_argument('outfile', nargs='?')

    
class ClientListener(Thread):

    def mkdir(self, args):
        if not args.infile:
            return "specify directory name"

        try:
            os.mkdir(args.infile)

        except OSError as e:
            return str(e)
        except FileExistsError:
            return "directory already exists"
        return "created"

    def ls(self, args):
        
        if args.infile:
            return '\n'.join(os.listdir(args.infile))

        else:
            return '\n'.join(os.listdir())

    def cd(self, args):
        if not args.infile:
            return "specify directory path"

        os.chdir(args.infile)
        return os.getcwd()

    def replicate(self, fd, n_copies):
        fd.seek(0)
        addrs = []
        for line in fd:
            addrs.append(line.split('_')[0])

        print(addrs)

        for i in range(n_copies - len(addrs)):
            while True:
                addr = random.choice(list(self.storage_manager.servers))
                print(str(addr))
                if addr not in addrs:
                    break

            salt = random.randint(0, 65536)
            full_name = fd.name + str(addr[0]) + str(salt)
            storage_name = str(hash(full_name.encode()))
            fd.write(str(addr) + '_' + storage_name + '\n')
            message = 'create ' + storage_name
            self.storage_manager.servers[addr].sendall(message.encode())
            # if all good, append new addr to addrs
            addrs.append(addr)
            print(f'sent to {addr}')

    
    def create(self, args):
        if not args.infile:
            return "specify file name"

        fd = open(args.infile, 'a+')

        self.replicate(fd, 2)
        fd.close()
        return 'created ' + args.infile


    def node_info(self, args):
        try:
            fd = open(args.infile, 'r')
        except FileNotFoundError:
            return "file does not exist"
        
        message = fd.read()
        return message
        


    def __init__(self, connection,  storage_manager):
        super().__init__(daemon=True)
        self.storage_manager = storage_manager
        self.connection = connection
        commands = [self.ls, self.mkdir, self.cd, self.create, self.node_info]
        self.commands = {func.__name__: func for func in commands}

        
    def parse_data(self, data):
        s = data.decode().split('\r')[0]
        return s.split(' ')

    def exec_command(self, args):
        #TODO
        args = parser.parse_args(args=args)
        command = args.command
        
        if command in self.commands:
            return self.commands[command](args) + '\n'
        
        return 'command not found\n'


    def run(self):

        while True:

            data = self.connection.recv(1024)
            if not data: # client ended communication
                self.connection.close()
                break

            
            args = self.parse_data(data)
            response = self.exec_command(args)
            self.connection.sendall(response.encode())
