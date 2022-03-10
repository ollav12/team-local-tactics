from rich.table import Table
from core import Champion, Match, Shape, Team
import socket, server, pickle
from database import save_match_history


# Return match summary
def return_match_summary(match: Match) -> None:

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

    info = []
    results = ""

    # For each round print a table with the results
    for index, round in enumerate(match.rounds):

        # Create a table containing the results of the round
        round_summary = Table(title=f'Round {index+1}')

        # Add columns for each team
        round_summary.add_column("Red",
                                 style="red",
                                 no_wrap=True)
        round_summary.add_column("Blue",
                                 style="blue",
                                 no_wrap=True)

        # Populate the table
        for key in round:
            red, blue = key.split(', ')
            round_summary.add_row(f'{red} {EMOJI[round[key].red]}',
                                  f'{blue} {EMOJI[round[key].blue]}')
        info.append(round_summary)

    red_score, blue_score = match.score
    results += f'Red: {red_score}\n'
    results += f'Blue: {blue_score}'

    if red_score > blue_score:
        results += '\n[red]Red victory! :grin:'
    elif red_score < blue_score:
        results += '\n[blue]Blue victory! :grin:'
    else:
        results += '\nDraw :expressionless:'
    
    save_match_history(results) # saves the match history 
    info.append(results)

    return info

# Return avalible champions function
def return_available_champs(champions: dict[Champion]) -> None:

    # Create a table containing available champions
    available_champs = Table(title='Available champions')

    # Add the columns Name, probability of rock, probability of paper and
    # probability of scissors
    available_champs.add_column("Name", style="cyan", no_wrap=True)
    available_champs.add_column("prob(:raised_fist-emoji:)", justify="center")
    available_champs.add_column("prob(:raised_hand-emoji:)", justify="center")
    available_champs.add_column("prob(:victory_hand-emoji:)", justify="center")

    # Populate the table
    for champion in champions.values():
        available_champs.add_row(*champion.str_tuple)

    return available_champs

# Validate champion pick function
def validate_champion_pick(champion, player_number, champions, you, opponent):

    if champion in you:
        player_number.send(f'[{champion} is already in your team. Try again.]'.encode()) # Same method as in teamlocaltactics.py but modifed to send error message to the player directly
    elif champion in opponent:
        player_number.send(f'[{champion} is in the enemy team. Try again.]'.encode())
    elif champion not in champions:
        player_number.send(f'[The champion {champion} is not available. Try again.]'.encode())
    else:
        return True

def get_scores(sel1: list, sel2: list, champions: dict[Champion], player1: socket, player2: socket):
    
    match = Match(
        Team([champions[name] for name in sel1]),
        Team([champions[name] for name in sel2])
    )
    match.play()

    game_results = return_match_summary(match) # Using the function from teamnetworktactics to get match_summary of match

    for i in range(len(game_results)):
        server.delay(0.1)
        player1.send("\n".encode())
        player2.send("\n".encode())

        server.delay(0.1)
        player1.send("next message is pickled".encode())
        player2.send("next message is pickled".encode())

        server.delay(0.1)
        pickle_champs = pickle.dumps(game_results[i])
        player1.send(pickle_champs)
        player2.send(pickle_champs)
