from rich.table import Table
from core import Champion, Match, Shape, Team
import socket, server, pickle
from database import save_match_history


# Return match summary
# I
def return_match_summary(match: Match) -> None:

    # Here we create varialbes to save summary and results
    summary = []
    results = ""

    EMOJI = {
        Shape.ROCK: ':raised_fist-emoji:',
        Shape.PAPER: ':raised_hand-emoji:',
        Shape.SCISSORS: ':victory_hand-emoji:'
    }

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
        summary.append(round_summary)

    # Adds the score to results string
    red_score, blue_score = match.score
    results += f'Red: {red_score}\n'
    results += f'Blue: {blue_score}'

    # Adds the winner to results string
    if red_score > blue_score:
        results += '\n[red]Red victory! :grin:'
    elif red_score < blue_score:
        results += '\n[blue]Blue victory! :grin:'
    else:
        results += '\nDraw :expressionless:'
    
    save_match_history(results) # saves the match history 
    summary.append(results)

    return summary

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

    return available_champs # identical to print_avalible_champs but instead if print we use return

# Validate champion pick function
# Identical to input_champion function from teamlocaltactics.py but here we send instead of printing
def validate_champion_pick(champion, player_number, champions, you, opponent):

    if champion in you:
        player_number.send(f'[{champion} is already in your team. Try again.]'.encode()) 
    elif champion in opponent:
        player_number.send(f'[{champion} is in the enemy team. Try again.]'.encode())
    elif champion not in champions:
        player_number.send(f'[The champion {champion} is not available. Try again.]'.encode())
    else:
        return True

    
# Get scores function
# Identical to parts of the main() function in teamlocaltactics.py
def get_match_results(player_one_team, player_two_team, champions, player_one, player_two):
    
    match = Match(
        Team([champions[name] for name in player_one_team]),
        Team([champions[name] for name in player_two_team])
    )
    match.play()

    game_results = return_match_summary(match)

    player_one.send("next message is pickled".encode())
    player_two.send("next message is pickled".encode())

    # Simple for loop in range of length of the list gane_results
    # Sends a new line first then "next message is pickled" and then the pickled message going through all of the strings in the list
    for i in range(len(game_results)):
        player_one.send("\n".encode())
        player_two.send("\n".encode())

        player_one.send("next message is pickled".encode())
        player_two.send("next message is pickled".encode())

        pickle_champs = pickle.dumps(game_results[i])
        player_one.send(pickle_champs)
        player_two.send(pickle_champs)
