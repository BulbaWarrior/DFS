import socket
from time import sleep

INIT_PORT = 1337
TALK_PORT = 1338

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
sleep(10)
sock.sendall(b'connected to you via tcp')
