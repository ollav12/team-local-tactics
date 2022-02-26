# This is where the client for the player is created. Here the game will be loaded and forwarded on to the server?
import socket

HEADER = 64
PORT = 5050 # port number
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)