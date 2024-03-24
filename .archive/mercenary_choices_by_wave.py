from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import json
from itertools import chain
import numpy as np
import seaborn as sns

FILE_NAME = "game_data.json"

with open(FILE_NAME, "r") as file:
    games = json.load(file)

filtered_games = [game for game in games if game['queueType'] == 'Normal' and game['gameElo'] > 2000]

# Collect all mercenaries sent per wave
mercenaries_sent_per_wave = list(chain.from_iterable([player['mercenariesSentPerWave'] for game in filtered_games for player in game['playersData']]))

# Flatten the nested list
mercenaries_sent = list(chain.from_iterable(mercenaries_sent_per_wave))
print(mercenaries_sent[:10])

# Count the occurrences of each mercenary
mercenary_counts = Counter(mercenaries_sent)
print(mercenary_counts)

# Calculate the total number of games
total_games = len(filtered_games)

# Calculate the average frequency per game for each mercenary
average_mercenary_frequency = {mercenary: count / total_games for mercenary, count in mercenary_counts.items()}
print(average_mercenary_frequency)

# Sort the mercenaries based on average frequency
sorted_mercenaries = sorted(average_mercenary_frequency.keys(), key=lambda x: average_mercenary_frequency[x], reverse=True)

# 1. Prepare data for the heatmap
heatmap_data = defaultdict(Counter)

# Populating the data dictionary
for mercenaries_in_wave in mercenaries_sent_per_wave:
    for wave_num, mercenary_list in enumerate(mercenaries_in_wave, 1):
        heatmap_data[wave_num].update(mercenary_list)

print(heatmap_data)

# 2. Convert the 2D dictionary to a 2D list (matrix)
max_wave = max(heatmap_data.keys())
mercenaries_list = sorted_mercenaries

matrix = []

for wave in range(1, 3):  # Print for the first two waves
    print(f"Wave {wave} data: {heatmap_data[wave]}")


for mercenary in mercenaries_list:
    row = []
    for wave in range(1, max_wave + 1):
        count = heatmap_data[wave].get(mercenary, 0)
        if count is None:  # This is just for diagnosis
            count = 0
        row.append(count)
    matrix.append(row)

matrix = np.array(matrix)
print(matrix)

# 3. Create the heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(matrix, annot=True, xticklabels=range(1, max_wave + 1), yticklabels=mercenaries_list, cmap="YlGnBu")
plt.xlabel('Wave Number')
plt.ylabel('Mercenary Type')
plt.title('Frequency of Each Mercenary Sent per Wave')
plt.show()
