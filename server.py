import socket, time, pickle
import teamnetworktactics as tnt
from threading import Thread
from rich import print
#from core import Champion, Match, Team
from database import load_some_champs

IP = 'localhost'
PORT = 1234

# Here we define the server_start function which is where we initialize the socket and starts to liten for other sockets
def server_initialize():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Saves the socket as variable server_sock. We use ipv4 and tcp protocol in our socket
    server_sock.bind((IP, PORT)) # Here we bind the IP and PORT
    server_sock.listen() # Here the server_sock starts to liten for connections
    print("[Server socket initialized. Server searching for connections...]") # Here we just print out a simple message in the server terminal just to let us know that the server has started

    # Now we accept the connections if they appear and then save them in a variable.
    # Player 1 = First client to connect to the server
    player_one, _ = server_sock.accept() # Here we accept connections
    player_one.send("1".encode()) # Once the first client has connected we then procced to send the first client a message to indicate which player number he is. 
    waiting_for_opponent(player_one)
    print("[Player 1 connected]") # SERVER TERMINAL

    # Player 2 = Second client to connect to the server
    player_two, _ = server_sock.accept()
    player_two.send("2".encode())
    waiting_for_opponent(player_two)
    print("[Player 2 connected]") # SERVER TERMINAL

    delay(1) # See delay function for description

    game_thread = Thread(target = game_loop, args = (player_one, player_two))
    game_thread.start()
    print("[Thread started]") # SERVER TERMINAL

# This function send the client a message while waiting for an opponent to connect
def waiting_for_opponent(player_number):
    delay(1)
    welcome_message = ('\n'
          '[Welcome to [bold yellow]Team Local Tactics[/bold yellow]!]'
          '\n'
          '[Waiting for opponent...]'
          '\n')
    player_number.send(welcome_message.encode()) # Here we send the welcome_message to the player and also encoding it to bytes


# This method is used for the game
def game_loop(player_one, player_two):

    delay(1)
    # Once the thread has started we then send both players the message "opponent foun"
    player_one.send("[Your opponent is ready! Match starting...]\n".encode())
    player_two.send("[Your opponent is ready! Match starting...]\n".encode())
    print("[Player 1 and Player 2 connected. Game Starting]") # SERVER TERMINAL
 
    delay(1) 
    # Here each player will recive a message which will display which player number they are.
    player_one.send("[You: [red]Player 1[white], Opponent: [blue]Player 2[white]]\n".encode())
    player_two.send("[You: [blue]Player 2[white], Opponent: [red]Player 1[white]]\n".encode())
    delay(1)
    player_one.send("[[bold yellow]Champion select starting in:[/bold yellow]] [white]\n".encode())
    player_two.send("[[bold yellow]Champion select starting in:[/bold yellow]] [white]\n".encode())
    delay(1)
    player_one.send("[3]".encode())
    player_two.send("[3]".encode())
    delay(1)
    player_one.send("[2]".encode())
    player_two.send("[2]".encode())
    delay(1)
    player_one.send("[1]\n".encode())
    player_two.send("[1]\n".encode())

    # Here we send "next message is pickled" to each client which then procceds to use this message in the client
    player_one.send("next message is pickled".encode())
    player_two.send("next message is pickled".encode())

    delay(1)
    # Now we use methods from other scripts to display avalible champions to the players
    champions = load_some_champs() # method from database.py
    available_champs = tnt.return_available_champs(champions) # method form teamnetworktactics.py
    pickled_avalible_champs = pickle.dumps(available_champs) # Here we pickle the avalible_champs

    #Then we send the pickled_avalible_champs to p1 and p2
    player_one.send(pickled_avalible_champs)
    player_two.send(pickled_avalible_champs) 
    
    # Here we create two empty lists, one for p1 and one for p2. Here we are gonna save the champions they pick
    player_one_team = []
    player_two_team = []

    # for loop where players are inputting two champs each in total one at a time
    for i in range(2):

        delay(0.1)
        player_one.send("1".encode()) # Player one recives "1" which signals that it is player one's turn
        player_two.send("\n[Waiting for [red]Player 1[white] to choose champion...]\n".encode()) # Player two recives "waiting for ..." and has to wait for player one to finish

        # While true loop where we are expecting a champion name from player one and then validating if the champion is valid or not.
        while True:
            player_one_champion = player_one.recv(1024).decode() # recive champion from player 1
            if tnt.validate_champion_pick(player_one_champion, player_one, champions, player_one_team, player_two_team) == True: # function from teamnetworktactics.py that checks if the champ is valid
                player_one.send("Valid".encode()) # Sends the message "Valid" to player one
                player_one_team.append(player_one_champion) # appends player_one_champion to player_one_team
                print("[Player 1 Picked Champion]") # SERVER TERMINAL
                break
        
        player_one_pick = "[red]Player 1[white]: " + player_one_champion # Here we save a message which says: Player 1: {first_pick}.
        player_two.send(player_one_pick.encode()) # message is sent to player_two

        delay(0.1)
        # Now player one needs to wait for player 2 to choose a champion
        player_one.send("\n[Waiting for [blue]Player 2[white] to choose champion...]\n".encode())
        player_two.send("2".encode()) # We send player two the message "2" which gives player two green signal to choose a champion

        # Same as which player one but now for player two
        while True:
            player_two_champion = player_two.recv(1024).decode()
            if tnt.validate_champion_pick(player_two_champion, player_two, champions, player_two_team, player_one_team) == True:
                player_two.send("Valid".encode())
                player_two_team.append(player_two_champion)
                print("[Player 2 picked champion]") # SERVER TERMINAL
                break
        
        # Here we procced to do the same again saving the output of player_two_pick and sending it to player_one
        player_two_pick = "[blue]Player 2[white]: " + player_two_champion
        player_one.send(player_two_pick.encode())

    delay(0.1)
    # Here we use the get_scores method.
    tnt.get_match_results(player_one_team, player_two_team, champions, player_one, player_two)

    delay(10)
    player_one.send("[[bold yellow]Game closing in:[/bold yellow]] [white]\n".encode())
    player_two.send("[[bold yellow]Game closing in:[/bold yellow]] [white]\n".encode())
    delay(1)
    player_one.send("[3]".encode())
    player_two.send("[3]".encode())
    delay(1)
    player_one.send("[2]".encode())
    player_two.send("[2]".encode())
    delay(1)
    player_one.send("[1]\n".encode())
    player_two.send("[1]\n".encode())
    
    delay(0.5)
    # Now that the game is finished we send the message to the client which then breaks out of the "champion input" loop
    player_one.send("game finished".encode())
    player_two.send("game finished".encode())
    print("[Game finished]") # SERVER TERMINAL

# This fucntions just creates a delay before doing something, created it because it made the code look better and more readable (in my opinion)
def delay(sec): # Here you input the amount of time you it to delay for
    time.sleep(sec)

# Server starting
server_initialize()