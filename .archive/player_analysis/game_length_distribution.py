import matplotlib.pyplot as plt

# Assuming 'filtered_ranked_games' is your list of ranked game data
game_lengths = [game['gameLength'] for game in filtered_ranked_games]

plt.figure(figsize=(10, 6))
plt.hist(game_lengths, bins=20, color='skyblue', edgecolor='black')
plt.title('Distribution of Game Lengths in Ranked Matches')
plt.xlabel('Game Length (seconds)')
plt.ylabel('Number of Games')
plt.show()
