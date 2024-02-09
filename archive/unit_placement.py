from collections import Counter
import matplotlib.pyplot as plt
import json

import numpy as np

FILE_NAME = "game_data.json"

with open(FILE_NAME, "r") as file:
    games = json.load(file)

filtered_games = [game for game in games if game['queueType'] == 'Normal' and game['gameElo'] > 2000]

unit_id = 'fire_elemental_unit_id'

# Define the grid dimensions
grid_rows = 10
grid_columns = 30

# Create an empty grid to store unit placement counts
unit_placement_grid = np.zeros((grid_rows, grid_columns))

# Example game data (replace this with your actual data)
example_game_data = [
    {
        "wave": 1,
        "unit_placements": [
            (0, 1), (2, 3), (4, 5),  # Example coordinates for wave 1
        ]
    },
    {
        "wave": 2,
        "unit_placements": [
            (1, 0), (3, 2), (5, 4),  # Example coordinates for wave 2
        ]
    },
    # ... (data for other waves)
]

# Fill the grid with unit placement counts
for data in example_game_data:
    wave = data["wave"]
    coordinates = data["unit_placements"]

    for row, column in coordinates:
        unit_placement_grid[row][column] += 1

# Transpose the grid
transposed_grid = unit_placement_grid.T  # or use np.transpose(unit_placement_grid)

# Create a heatmap
plt.figure(figsize=(12, 8))
plt.imshow(transposed_grid, cmap="viridis", aspect="auto")
plt.colorbar(label="Unit Placement Count")
plt.xlabel("Row")
plt.ylabel("Column")
plt.title("Unit Placement Heatmap by Wave")
plt.show()