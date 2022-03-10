import socket, pickle
from rich import print
from rich.prompt import Prompt

IP = 'localhost'
PORT = 1234

# Function that initializes the client.
def client_initialize():
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Creats client_sock with ipv4 and tcp protocol
    client_sock.connect((IP, PORT)) # Connects to the IP and PORT
    player_number = client_sock.recv(1024).decode()
    game_loop(client_sock, player_number)

def game_loop(client_sock, player_number):
    while True:
        message = client_sock.recv(1024).decode()
        if message == player_number:
            while True:
                if player_number == "1":
                    text = "[red]Player " + player_number + ":[white]"
                else:
                    text = "[blue]Player " + player_number + ":[white]"

                player_number_champion = Prompt.ask(text) # Here we use pompt.ask instead of input becuse if we used input player would not display any color
                client_sock.send(player_number_champion.encode())
                valid = client_sock.recv(1024).decode()
                if valid == "Valid":
                    break
                else:
                    print(valid)
        elif message == "next message is pickled":
            pickled_message = client_sock.recv(4096)
            unpickled_message = pickle.loads(pickled_message)
            print(unpickled_message)
        elif message == "game finished":
            break
        else:
            print(message)

#Starting client
client_initialize()