from threading import Thread
import os
import argparse



def mkdir(args):
    if not args.infile:
        return "specify directory name"

    try:
        os.mkdir(args.infile)

    except OSError as e:
        return str(e)
    except FileExistsError:
        return "directory already exists"
    return "created"


def ls(args):
    if args.infile:
        return '\n'.join(os.listdir(args.infile))

    else:
        return '\n'.join(os.listdir())

def cd(args):
    if not args.infile:
        return "specify directory path"

    os.chdir(args.infile)
    return os.getcwd()


# single_commands = ['init', 'ls']
# unary_commands = ['create', 'read', 'rm', 'info', 'cd', 'rmdir']
# binary_commands = ['write', 'cp', 'mv']
# commands = [*single_commands, *unary_commands, *binary_commands]
commands = [ls, mkdir, cd]
commands = {func.__name__: func for func in commands}
parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('infile', nargs='?')
parser.add_argument('outfile', nargs='?')

    
class ClientListener(Thread):

    def __init__(self, connection,  storage_manager):
        super().__init__(daemon=True)
        self.storage_manager = storage_manager
        self.connection = connection

        
    def parse_data(self, data):
        s = data.decode().split('\r')[0]
        return s.split(' ')

    def exec_command(self, args):
        #TODO
        args = parser.parse_args(args=args)
        command = args.command
        
        if command in commands:
            return commands[command](args) + '\n'
        
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
