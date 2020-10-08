import socket
from initialization import ProbeListener, StorageManager, ClientListener

INIT_PORT = 1337
TALK_PORT = 1338
CLIENT_PORT = 22322


probe_sock = socket.socket(socket.AF_INET,
                           socket.SOCK_DGRAM)
probe_sock.bind(('', INIT_PORT))

ProbeListener(probe_sock).start()


storage_sock = socket.socket(socket.AF_INET,
                             socket.SOCK_STREAM)
storage_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
storage_sock.bind(('', TALK_PORT))
storage_sock.listen(5)

storage_manager = StorageManager(storage_sock)

storage_manager.start()


welcome_socket = socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM)
welcome_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
welcome_socket.bind(('', CLIENT_PORT))
welcome_socket.listen(10)

while True:
    conn, addr = welcome_socket.accept()
    ClientListener(conn, storage_manager).start()

    
