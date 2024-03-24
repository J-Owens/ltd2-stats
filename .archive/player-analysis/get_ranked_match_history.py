import os
import requests
from collections import Counter
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import csv
import json


API_URL = 'https://apiv2.legiontd2.com'
API_KEY = os.environ["LEGION_API_KEY"]
HEADERS = {'x-api-key': API_KEY}

def get_player_match_history(id):
    response = requests.get(f'{API_URL}/players/matchHistory/{id}?limit=50&offset=50', headers=HEADERS)
    return response.json()


def get_player_id(nickname):
    response = requests.get(f'{API_URL}/players/byName/{nickname}', headers=HEADERS)
    player_profile = response.json()
    return player_profile['_id']


def get_ranked_games(player):
    player_name = player
    player_id = get_player_id(player_name)
    games = get_player_match_history(player_id)
    ranked_games = [game for game in games if game['queueType'] == 'Normal']
    with open(f'{player}_ranked_games.json', 'w') as file:
        json.dump(ranked_games, file, indent=4)


def main():
    get_ranked_games('Kingdanzz')
    #get_ranked_games('xPrawn')
    #get_ranked_games('ElPulpoDeBadia')


if __name__ == "__main__":
    main()
