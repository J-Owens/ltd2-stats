import json
from collections import defaultdict
import matplotlib.pyplot as plt
import os

data_directory = 'data/match_data'

def get_filepaths():
    filepaths = []
    for filename in os.listdir(data_directory):
        if filename.endswith('.json'):
            filepath = os.path.join(data_directory, filename)
            filepaths.append(filepath)
    return filepaths

def most_used_units_by_legion(match_files):
    legion_unit_counts = defaultdict(lambda: defaultdict(int))
    legion_total_units = defaultdict(int)
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                legion = player_data['legion']
                for build in player_data['buildPerWave']:
                    for unit in build:
                        unit_id = unit.split(':')[0]
                        legion_unit_counts[legion][unit_id] += 1
                        legion_total_units[legion] += 1
    
    for legion, unit_counts in legion_unit_counts.items():
        print(f"{legion} most used units:")
        sorted_units = sorted(unit_counts.items(), key=lambda x: x[1], reverse=True)
        total_units = legion_total_units[legion]
        for unit_id, count in sorted_units:
            percentage = count / total_units * 100
            print(f"{unit_id}: {count} ({percentage:.2f}%)")
        print()

def average_workers_and_income_per_wave(match_files):
    worker_counts = defaultdict(list)
    incomes = defaultdict(list)

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                for wave, workers in enumerate(player_data['workersPerWave'], 1):
                    worker_counts[wave].append(workers)
                for wave, income in enumerate(player_data['incomePerWave'], 1):
                    incomes[wave].append(income)

    waves = list(range(1, len(worker_counts) + 1))
    avg_workers = [sum(worker_counts[wave]) / len(worker_counts[wave]) for wave in waves]
    avg_income = [sum(incomes[wave]) / len(incomes[wave]) for wave in waves]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Wave')
    ax1.set_ylabel('Avg. Workers', color=color)
    ax1.plot(waves, avg_workers, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('Avg. Income', color=color)
    ax2.plot(waves, avg_income, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()
    plt.title('Average Workers and Income per Wave')
    plt.show()


def mercenary_usage_patterns(match_files):
    sent_mercenaries = defaultdict(lambda: defaultdict(int))
    received_mercenaries = defaultdict(lambda: defaultdict(int))
    total_sent_mercs = defaultdict(int)
    total_received_mercs = defaultdict(int)

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                for wave, mercs in enumerate(player_data['mercenariesSentPerWave'], 1):
                    for merc in mercs:
                        sent_mercenaries[wave][merc] += 1
                        total_sent_mercs[wave] += 1
                for wave, mercs in enumerate(player_data['mercenariesReceivedPerWave'], 1):
                    for merc in mercs:
                        received_mercenaries[wave][merc] += 1
                        total_received_mercs[wave] += 1

    avg_sent_mercs = sum(total_sent_mercs.values()) / len(total_sent_mercs)
    avg_received_mercs = sum(total_received_mercs.values()) / len(total_received_mercs)

    print("Sent Mercenaries:")
    for wave, mercs in sent_mercenaries.items():
        print(f"Wave {wave}:")
        total_wave_mercs = total_sent_mercs[wave]
        for merc, count in mercs.items():
            percentage = count / total_wave_mercs * 100
            deviation = (count - avg_sent_mercs) / avg_sent_mercs * 100
            print(f"{merc}: {count} ({percentage:.2f}%), {deviation:+.2f}% from average")
        print()

    print("\nReceived Mercenaries:")
    for wave, mercs in received_mercenaries.items():
        print(f"Wave {wave}:")
        total_wave_mercs = total_received_mercs[wave]
        for merc, count in mercs.items():
            percentage = count / total_wave_mercs * 100
            deviation = (count - avg_received_mercs) / avg_received_mercs * 100
            print(f"{merc}: {count} ({percentage:.2f}%), {deviation:+.2f}% from average")
        print()


def king_upgrade_sequences(match_files):
    upgrade_sequences = []
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                if player_data['gameResult'] == 'won':
                    upgrade_sequences.append(player_data['kingUpgradesPerWave'])
    
    upgrade_counts = defaultdict(int)
    for sequence in upgrade_sequences:
        upgrade_counts[tuple(tuple(wave) for wave in sequence)] += 1
    
    print("Most Common King Upgrade Sequences in Won Games:")
    sorted_sequences = sorted(upgrade_counts.items(), key=lambda x: x[1], reverse=True)
    for sequence, count in sorted_sequences[:5]:
        print(f"Count: {count}")
        for wave, upgrades in enumerate(sequence, 1):
            print(f"Wave {wave}: {', '.join(upgrades)}")
        print()


def first_wave_unit_win_rates(match_files):
    unit_wins = defaultdict(int)
    unit_games = defaultdict(int)
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                first_wave_units = player_data['firstWaveFighters'].split(',')
                for unit in first_wave_units:
                    unit_games[unit] += 1
                    if player_data['gameResult'] == 'won':
                        unit_wins[unit] += 1
    
    win_rates = {}
    for unit, wins in unit_wins.items():
        games = unit_games[unit]
        win_rates[unit] = wins / games * 100

    # Sort win rates (descending order)
    sorted_win_rates = dict(sorted(win_rates.items(), key=lambda item: item[1], reverse=True))

    # Print results (you can modify this to your liking)
    for unit, win_rate in sorted_win_rates.items():
        print(f"{unit}: {win_rate:.2f}% ({unit_games[unit]} games)") 


def spell_choices_and_locations(match_files):
    spell_choices = defaultdict(int)
    spell_locations = defaultdict(int)
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                spell = player_data['chosenSpell']
                location = player_data['chosenSpellLocation']
                spell_choices[spell] += 1
                spell_locations[location] += 1
    
    print("Spell Choices:")
    sorted_spells = sorted(spell_choices.items(), key=lambda x: x[1], reverse=True)
    for spell, count in sorted_spells:
        print(f"{spell}: {count}")
    
    print("\nSpell Locations:")
    sorted_locations = sorted(spell_locations.items(), key=lambda x: x[1], reverse=True)
    for location, count in sorted_locations:
        print(f"{location}: {count}")


def late_game_unit_compositions(match_files):
    unit_counts = defaultdict(int)
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                if player_data['gameResult'] == 'won':
                    last_wave_units = player_data['buildPerWave'][-1]
                    for unit in last_wave_units:
                        unit_id = unit.split(':')[0]
                        unit_counts[unit_id] += 1
    
    print("Most Used Units in Last Wave of Won Games:")
    sorted_units = sorted(unit_counts.items(), key=lambda x: x[1], reverse=True)
    for unit_id, count in sorted_units[:10]:
        print(f"{unit_id}: {count}")


files = get_filepaths()
average_workers_and_income_per_wave(files)