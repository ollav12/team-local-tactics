from core import Champion
import csv, pickle

def _parse_champ(champ_text: str) -> Champion:
    name, rock, paper, scissors = champ_text.split(sep=',')
    return Champion(name, float(rock), float(paper), float(scissors))


def from_csv(filename: str) -> dict[str, Champion]:
    champions = {}
    with open(filename, 'r') as f:
        for line in f.readlines():
            champ = _parse_champ(line)
            champions[champ.name] = champ
    return champions

# Database function, if i edit stats in champions.txt it will modify the way the champions works.
def load_some_champs():
    return from_csv('champions.txt')

# Saves match history in match_history.txt
def save_match_history(results):
    with open('match_history.txt', 'a', newline = '\n') as f:
        f.write("\n")
        f.write(f"{results}")