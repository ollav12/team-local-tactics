# This is ths server where the game will be running on
import socket
import threading
#import teamlocaltactics as tlt

HEADER = 64
PORT = 5050 # port number
SERVER = socket.gethostbyname(socket.gethostname()) # This assigns the variable SERVER with your localhost ip adress automaticly.
ADDRESS = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creating a socket using a tcp socket
server.bind(ADDRESS) # Binds the socket together with the adress


def handle_client(connection, address):
    print(f"[NEW CONNECTION] {address} connected")

    connected = True
    while connected:
            msg_length = connection.recv(HEADER).decode(FORMAT)
            if msg_length: 
                msg_length = int(msg_length)
                msg = connection.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = False

                print(f"[{address}] {msg}")
                connection.send("Msg received".encode(FORMAT))

    connection.close()


def start(): # Function that starts to liste for connections 
    server.listen() # Enables the server to listen for connections
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target = handle_client, args = (connection, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")



print("[STARTING] server is starting...")
start()
