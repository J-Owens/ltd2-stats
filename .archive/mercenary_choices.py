from collections import Counter
import matplotlib.pyplot as plt
import json
from itertools import chain

FILE_NAME = "game_data.json"

with open(FILE_NAME, "r") as file:
    games = json.load(file)

filtered_games = [game for game in games if game['queueType'] == 'Normal' and game['gameElo'] > 2000]

# Collect all mercenaries sent per wave
mercenaries_sent_per_wave = list(chain.from_iterable([player['mercenariesSentPerWave'] for game in filtered_games for player in game['playersData']]))

# Flatten the nested list
mercenaries_sent = list(chain.from_iterable(mercenaries_sent_per_wave))

# Count the occurrences of each mercenary
mercenary_counts = Counter(mercenaries_sent)

# Calculate the total number of games
total_games = len(filtered_games)

# Calculate the average frequency per game for each mercenary
average_mercenary_frequency = {mercenary: count / total_games for mercenary, count in mercenary_counts.items()}

# Sort the mercenaries based on average frequency
sorted_mercenaries = sorted(average_mercenary_frequency.keys(), key=lambda x: average_mercenary_frequency[x], reverse=True)
sorted_average_frequency = [average_mercenary_frequency[mercenary] for mercenary in sorted_mercenaries]

# Create a bar chart to show average mercenary frequency per game
plt.figure(figsize=(10, 6))
plt.bar(sorted_mercenaries, sorted_average_frequency)
plt.xlabel('Mercenary Sent')
plt.ylabel('Average Frequency per Game')
plt.title('Average Mercenary Frequency per Game')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.tight_layout()
plt.show()