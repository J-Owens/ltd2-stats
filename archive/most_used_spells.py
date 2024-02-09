from collections import Counter
import matplotlib.pyplot as plt
import json

FILE_NAME = "game_data.json"

with open(FILE_NAME, "r") as file:
    games = json.load(file)

filtered_games = [game for game in games if game['queueType'] == 'Normal' and game['gameElo'] > 2000]

# Collect spell choices from each player's data
spell_choices = [player['chosenSpell'] for game in filtered_games for player in game['playersData']]

# Count the occurrences of each spell
spell_counts = Counter(spell_choices)

# Create a bar chart to show spell frequency
plt.figure(figsize=(10, 6))
plt.bar(spell_counts.keys(), spell_counts.values())
plt.xlabel('Spell Choice')
plt.ylabel('Frequency')
plt.title('Most Used Spells')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.show()