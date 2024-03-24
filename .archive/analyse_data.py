import matplotlib.pyplot as plt
import json

FILE_NAME = "game_data.json"

with open(FILE_NAME, "r") as file:
    games = json.load(file)

filtered_games = [game for game in games if game['queueType'] == 'Normal' and game['gameElo'] > 2000]

wave_numbers = list(range(1, 22))
left_king_hp_by_wave = []
right_king_hp_by_wave = []

for wave in wave_numbers:
    left_king_hp_sum = 0
    right_king_hp_sum = 0
    count = 0

    for game in filtered_games:
        if wave <= len(game['leftKingPercentHp']):
            left_king_hp_sum += game['leftKingPercentHp'][wave - 1]
            right_king_hp_sum += game['rightKingPercentHp'][wave - 1]
            count += 1

    if count > 0:
        left_king_hp_by_wave.append(left_king_hp_sum / count)
        right_king_hp_by_wave.append(right_king_hp_sum / count)
    else:
        left_king_hp_by_wave.append(0)
        right_king_hp_by_wave.append(0)

plt.figure(figsize=(10, 6))
plt.plot(wave_numbers, left_king_hp_by_wave, label='Left King HP')
plt.plot(wave_numbers, right_king_hp_by_wave, label='Right King HP')
plt.xlabel('Wave Number')
plt.ylabel('King HP (%)')
plt.title('King HP by Wave')
plt.legend()
plt.grid()
plt.show()