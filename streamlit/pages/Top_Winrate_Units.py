import json
from collections import defaultdict
import os
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Top Winrate Units by Legion", layout="wide")

st.markdown("# Top Winrate Units by Legion")

def top_winning_units(match_files):
    total_unit_win_count = defaultdict(int)
    total_unit_loss_count = defaultdict(int)
    legion_unit_wins = defaultdict(lambda: defaultdict(int))
    legion_unit_losses = defaultdict(lambda: defaultdict(int))
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                legion = player_data['legion']
                for unit in player_data['buildPerWave'][-1]:
                    unit_id = unit.split(':')[0][:-8]
                    if player_data['gameResult'] == 'won':
                        total_unit_win_count[unit_id] += 1
                        legion_unit_wins[legion][unit_id] += 1
                    else:
                        total_unit_loss_count[unit_id] += 1
                        legion_unit_losses[legion][unit_id] += 1

    charts = []

    unit_winrates = {}
    for unit_id, win_count in total_unit_win_count.items():
        total_count = total_unit_win_count[unit_id] + total_unit_loss_count[unit_id]
        if total_count >= 25:
            winrate = win_count / total_count * 100
            unit_winrates[unit_id] = winrate

    sorted_unit_winrates = sorted(unit_winrates.items(), key=lambda x: x[1])
    unit_ids = [unit_id for unit_id, _ in sorted_unit_winrates]
    winrates = [winrate for _, winrate in sorted_unit_winrates]
    counts = [total_unit_win_count[unit_id] + total_unit_loss_count[unit_id] for unit_id in unit_ids]

    winrate_chart_data = {
        'Unit ID': unit_ids,
        'Winrate': winrates,
        'Total Count': counts
    }

    chart = px.bar(winrate_chart_data, x='Winrate', y='Unit ID', hover_data=['Total Count'], orientation='h')
    chart.update_layout(title=f"Unit Winrates (Minimum 50 samples)")
    num_units = len(unit_ids)
    chart_height = num_units * 20  # Adjust the multiplier as needed
    chart.update_layout(width=800, height=chart_height)
    charts.append(chart)

    for legion in legion_unit_wins.keys():
        unit_winrates = {}
        for unit_id in legion_unit_wins[legion].keys():
            wins = legion_unit_wins[legion][unit_id]
            losses = legion_unit_losses[legion][unit_id]
            total_count = wins + losses
            if total_count > 25:
                winrate = wins / total_count * 100
                unit_winrates[unit_id] = (winrate, total_count)

        sorted_units = sorted(unit_winrates.items(), key=lambda x: x[1][0])
        unit_ids = [unit_id for unit_id, _ in sorted_units]
        winrates = [winrate for _, (winrate, _) in sorted_units]
        total_counts = [total_count for _, (_, total_count) in sorted_units]

        chart_data = {
            'Unit ID': unit_ids,
            'Winrate': winrates,
            'Total Count': total_counts
        }

        chart = px.bar(chart_data, x='Winrate', y='Unit ID', hover_data=['Total Count'], orientation='h')
        chart.update_layout(title=f"{legion} Unit Winrates (Minimum 25 samples)")

        # Calculate the dynamic height based on the number of unique unit names
        num_units = len(unit_ids)
        chart_height = num_units * 20  # Adjust the multiplier as needed

        # Set the width and dynamic height of the chart
        chart.update_layout(width=800, height=chart_height)
        charts.append(chart)

    return charts


# Specify the directory where the match files are located
match_directory = "data/match_data"

# Get the list of match files
match_files = [f"{match_directory}/{file}" for file in os.listdir(match_directory) if file.endswith('.json')]

if match_files:
    charts = top_winning_units(match_files)

    for chart in charts:
        st.plotly_chart(chart)
else:
    st.warning("No match files found in the specified directory.")