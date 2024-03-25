import streamlit as st
import json
import os
import plotly.express as px

st.set_page_config(page_title="Champion Units", layout="wide")

st.markdown("# Champion Units")


def champion_spell_units_count(match_files):
    champion_spell_units = {}

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            # Iterate over the players in the match
            for player in match_data['playersData']:
                if player['legion'] == 'Champion':
                    # Check if the player used the Champion spell
                    if 'chosenChampionLocation' in player and player['chosenChampionLocation'] != '-1|-1':
                        unit_location = player['chosenChampionLocation']

                        # Find the unit at the specified location in the build data
                        for wave_data in player['buildPerWave']:
                            for unit_data in wave_data:
                                if unit_location in unit_data:
                                    unit_name = unit_data.split(':')[0][:-8]
                                    if unit_name in champion_spell_units:
                                        champion_spell_units[unit_name] += 1
                                    else:
                                        champion_spell_units[unit_name] = 1
                                    break

    # Sort the unit names and counts based on count values in descending order
    sorted_units = sorted(champion_spell_units.items(), key=lambda x: x[1])
    unit_names = [unit[0] for unit in sorted_units]
    unit_counts = [unit[1] for unit in sorted_units]

    # Create a horizontal bar chart using Plotly Express
    chart_data = {'Unit Name': unit_names, 'Count': unit_counts}
    chart = px.bar(chart_data, x='Count', y='Unit Name', orientation='h', title='Champion Chosen Count')
    num_units = len(unit_names)
    chart_height = num_units * 20  # Adjust the multiplier as needed
    chart.update_layout(width=800, height=chart_height)

    # Display the chart using Streamlit
    st.plotly_chart(chart)


def champion_spell_units_winrate(match_files):
    champion_spell_units_wins = {}
    champion_spell_units_losses = {}

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            # Iterate over the players in the match
            for player in match_data['playersData']:
                if player['legion'] == 'Champion':
                    # Check if the player used the Champion Legion spell
                    if 'chosenChampionLocation' in player and player['chosenChampionLocation'] != '-1|-1':
                        unit_location = player['chosenChampionLocation']
                        # Find the unit at the specified location in the build data
                        for wave_data in player['buildPerWave']:
                            for unit_data in wave_data:
                                if unit_location in unit_data:
                                    unit_name = unit_data.split(':')[0][:-8]
                                    if player['gameResult'] == 'won':
                                        if unit_name in champion_spell_units_wins:
                                            champion_spell_units_wins[unit_name] += 1
                                        else:
                                            champion_spell_units_wins[unit_name] = 1
                                    else:
                                        if unit_name in champion_spell_units_losses:
                                            champion_spell_units_losses[unit_name] += 1
                                        else:
                                            champion_spell_units_losses[unit_name] = 1
                                    break

    # Calculate the winrate for each unit
    unit_winrates = {}
    for unit_name in champion_spell_units_wins.keys():
        wins = champion_spell_units_wins[unit_name]
        losses = champion_spell_units_losses.get(unit_name, 0)
        total_games = wins + losses
        if total_games >= 25:
            winrate = wins / total_games * 100
            unit_winrates[unit_name] = (winrate, total_games)

    # Sort the units based on winrate in descending order
    sorted_units = sorted(unit_winrates.items(), key=lambda x: x[1][0])
    unit_names = [unit[0] for unit in sorted_units]
    winrates = [unit[1][0] for unit in sorted_units]
    total_games = [unit[1][1] for unit in sorted_units]

    # Create a horizontal bar chart using Plotly Express
    chart_data = {'Unit Name': unit_names, 'Winrate': winrates, 'Total Games': total_games}
    chart = px.bar(chart_data, x='Winrate', y='Unit Name', orientation='h',
                   title='Champion Chosen Unit Winrates (Minimum 25 samples)', hover_data=['Total Games'])

    num_units = len(unit_names)
    chart_height = num_units * 20  # Adjust the multiplier as needed
    chart.update_layout(width=800, height=chart_height)

    # Display the chart using Streamlit
    st.plotly_chart(chart)


# Specify the directory where the match files are located
match_directory = "data/match_data"

# Get the list of match files
match_files = [f"{match_directory}/{file}" for file in os.listdir(match_directory) if file.endswith('.json')]

champion_spell_units_winrate(match_files)
champion_spell_units_count(match_files)