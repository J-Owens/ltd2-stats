from collections import defaultdict
from itertools import combinations
import json
import os


data_directory = 'data/match_data'

def get_filepaths():
    filepaths = []
    for filename in os.listdir(data_directory):
        if filename.endswith('.json'):
            filepath = os.path.join(data_directory, filename)
            filepaths.append(filepath)
    return filepaths


def analyze_successful_combinations(match_files, min_support=0.1):
    combination_counts = defaultdict(int)
    total_won_games = 0

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                if player_data['gameResult'] == 'won':
                    total_won_games += 1
                    units = set()
                    spell = player_data['chosenSpell']
                    mercenaries = set()

                    for build in player_data['buildPerWave']:
                        for unit in build:
                            unit_id = unit.split(':')[0]
                            units.add(unit_id)

                    for wave_mercs in player_data['mercenariesSentPerWave']:
                        for merc in wave_mercs:
                            mercenaries.add(merc)

                    for combo_size in range(2, 6):
                        for combo in combinations(units | {spell} | mercenaries, combo_size):
                            combination_counts[combo] += 1

    for combo, count in combination_counts.items():
        support = count / total_won_games
        if support >= min_support:
            print(f"Combination: {', '.join(combo)}, Support: {support:.2f}")


files = get_filepaths()
analyze_successful_combinations(files)