import socket
from time import sleep
from listeners import ServerListener, ClientListener
import os
INIT_PORT = 1337
TALK_PORT = 1338
CLIENT_PORT = 22322

os.chdir('/storage')

def probe_naming_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        sock.sendto(b"hello", ("255.255.255.255", INIT_PORT))
        data, addr = sock.recvfrom(1024)
        print(f"recieved message: {data} from address {addr}")
        if data == b'connect to me!':
            break
    sock.close()
    return addr

addr = probe_naming_server()


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

sock.connect((addr[0], TALK_PORT))
sock.sendall(b'connected to you via tcp')

ServerListener(sock).start()

client_sock = socket.socket(socket.AF_INTET, socket.SOCK_STREAM)
client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_sock.bind(('', CLIENT_PORT))
client_sock.listen(5)


while True:
    sock, addr = client_sock.accept()
    ClientListener(sock).start()
