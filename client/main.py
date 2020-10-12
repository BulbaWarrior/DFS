import argparse

import socket
import random

PORT = 22322
HOST = 'naming_server'

parser = argparse.ArgumentParser()
parser.add_argument('command')
parser.add_argument('infile', nargs='?')
parser.add_argument('outfile', nargs='?')


naming_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
naming_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

naming_sock.connect((HOST, PORT))


def locate_file(name):
    #TODO: might not have a file
    request = 'node_info ' + name
    naming_sock.sendall(request.encode())
    response = namig_sock.recv(1024)
    entries = response.decode.split('\n')[:-1]
    file_info = []
    for entry in entries:
        parsed_entry = tuple(entry.split('_'))
        file_info.append(parsed_entry)
    print(f'parsed file {name} for data: {file_info}')
    return file_info

def connect_storage(addr):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((addr, PORT))
    return sock

def push(data, sock):
    sock.sendall(data)             
    sock.close()


def pull(fd, sock):
    while True:
        data = sock.recv(1024)
        if not data: # connection closed
            break
        fd.write(data)

        fd.close()
        sock.close()

    

def write(args):
    if not args.infile:
        return "specify file name"


    with open(args.infile, 'r') as fd:
        send_data = fd.read()
        
    file_info = locate_file(args.infile)
    for entry in file_info:
        addr = entry[0]
        conn = connect_storage(addr)
        conn.sendall('write ' + entry[1])
        data = conn.recv(1024)
        if data.decode() != 'ready':
            return 'recieved wrong acknowledgement: ' + data.decode()

        push(send_data, conn)
        conn.close()
    return "finished writing"
        

def read(args):
    if not args.infile:
        return "specify file name"

    fd = open(args.infile, 'w')
    file_info = locate_file(args.infile)
    entry = random.choice(file_info)
    conn = connect_storage(entry[0])
    conn.sendall('read ' + entry[1])
    pull(fd, conn)
    fd.close()
    conn.close()
    return "finished reading"

    
    
complex_commands = [write, read,]
complex_commands = {func.__name__: func for func in complex_commands}    

def run_command(request):
    args = parser.parse_args(args=request.split())
    command = args.command
    if command in complex_commands:
        response = complex_commands[command](args)
        print(response)
        return
    
    naming_sock.sendall(request.encode())
    response = naming_sock.recv(1024)
    print(response.decode(), end='')

while True:
    command = input('$>')

    run_command(command)
