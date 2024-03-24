from collections import Counter
import matplotlib.pyplot as plt

# Assuming 'filtered_ranked_games' is your list of ranked game data
ending_waves = [game['endingWave'] for game in filtered_ranked_games]
wave_counts = Counter(ending_waves)

# Sorting waves for better visualization
sorted_waves = sorted(wave_counts.items())

waves, counts = zip(*sorted_waves)  # Unzipping the sorted wave-count pairs

plt.figure(figsize=(12, 6))
plt.bar(waves, counts, color='lightgreen', edgecolor='black')
plt.title('Ending Wave Frequencies in Ranked Matches')
plt.xlabel('Ending Wave')
plt.ylabel('Number of Games')
plt.xticks(waves)  # Ensure all wave numbers are shown as x-ticks
plt.show()
