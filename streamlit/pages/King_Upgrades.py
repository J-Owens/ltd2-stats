import streamlit as st
import json
import os
import plotly.graph_objects as go

def plot_average_king_upgrades_per_wave(match_files):
    king_upgrades_per_wave = {}

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            
            for player_data in match_data['playersData']:
                king_upgrades_per_wave_data = player_data['kingUpgradesPerWave']
                
                for wave, upgrades in enumerate(king_upgrades_per_wave_data, start=1):
                    if wave not in king_upgrades_per_wave:
                        king_upgrades_per_wave[wave] = []
                    king_upgrades_per_wave[wave].append(len(upgrades))

    waves = list(range(1, len(king_upgrades_per_wave) + 1))
    avg_king_upgrades = []

    for upgrades in king_upgrades_per_wave.values():
        if upgrades:
            avg_king_upgrades.append(sum(upgrades) / len(upgrades))
        else:
            avg_king_upgrades.append(0)

    fig = go.Figure(data=go.Scatter(x=waves, y=avg_king_upgrades, mode='lines+markers'))
    fig.update_layout(
        title='Average King Upgrades per Wave',
        xaxis_title='Wave',
        yaxis_title='Average King Upgrades'
    )

    st.plotly_chart(fig)


def plot_average_king_upgrades_per_wave_per_legion(match_files):
    king_upgrades_per_wave_per_legion = {}

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            
            for player_data in match_data['playersData']:
                legion = player_data['legion']
                king_upgrades_per_wave_data = player_data['kingUpgradesPerWave']
                
                if legion not in king_upgrades_per_wave_per_legion:
                    king_upgrades_per_wave_per_legion[legion] = {}
                
                for wave, upgrades in enumerate(king_upgrades_per_wave_data, start=1):
                    if wave not in king_upgrades_per_wave_per_legion[legion]:
                        king_upgrades_per_wave_per_legion[legion][wave] = []
                    king_upgrades_per_wave_per_legion[legion][wave].append(len(upgrades))

    for legion, king_upgrades_per_wave in king_upgrades_per_wave_per_legion.items():
        waves = list(range(1, len(king_upgrades_per_wave) + 1))
        avg_king_upgrades = []

        for upgrades in king_upgrades_per_wave.values():
            if upgrades:
                avg_king_upgrades.append(sum(upgrades) / len(upgrades))
            else:
                avg_king_upgrades.append(0)

        fig = go.Figure(data=go.Scatter(x=waves, y=avg_king_upgrades, mode='lines+markers'))
        fig.update_layout(
            title=f'Average King Upgrades per Wave - {legion}',
            xaxis_title='Wave',
            yaxis_title='Average King Upgrades'
        )

        st.plotly_chart(fig)


def plot_average_cumulative_king_upgrades_per_wave_per_type(match_files):
    king_upgrades_per_wave_per_type = {
        "Upgrade King Attack": {},
        "Upgrade King Spell": {},
        "Upgrade King Regen": {}
    }

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            
            for player_data in match_data['playersData']:
                king_upgrades_per_wave_data = player_data['kingUpgradesPerWave']
                
                for wave, upgrades in enumerate(king_upgrades_per_wave_data, start=1):
                    for upgrade_type in king_upgrades_per_wave_per_type.keys():
                        if wave not in king_upgrades_per_wave_per_type[upgrade_type]:
                            king_upgrades_per_wave_per_type[upgrade_type][wave] = []
                        king_upgrades_per_wave_per_type[upgrade_type][wave].append(upgrades.count(upgrade_type))

    waves = list(range(1, max(len(upgrades) for upgrades in king_upgrades_per_wave_per_type.values()) + 1))

    fig = go.Figure()

    for upgrade_type, king_upgrades_per_wave in king_upgrades_per_wave_per_type.items():
        cumulative_upgrades = [0] * len(waves)

        for wave in waves:
            if wave in king_upgrades_per_wave:
                upgrades = king_upgrades_per_wave[wave]
                if upgrades:
                    cumulative_upgrades[wave - 1] = cumulative_upgrades[wave - 2] + (sum(upgrades) / len(upgrades))
                else:
                    cumulative_upgrades[wave - 1] = cumulative_upgrades[wave - 2]
            else:
                cumulative_upgrades[wave - 1] = cumulative_upgrades[wave - 2]

        fig.add_trace(go.Scatter(x=waves, y=cumulative_upgrades, mode='lines+markers', name=upgrade_type))

    fig.update_layout(
        title='Average Cumulative King Upgrades per Wave per Type',
        xaxis_title='Wave',
        yaxis_title='Average Cumulative King Upgrades'
    )

    st.plotly_chart(fig)


def plot_average_cumulative_king_upgrades_per_wave_per_type_per_legion(match_files):
    king_upgrades_per_wave_per_type_per_legion = {}

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            
            for player_data in match_data['playersData']:
                legion = player_data['legion']
                if legion not in king_upgrades_per_wave_per_type_per_legion:
                    king_upgrades_per_wave_per_type_per_legion[legion] = {
                        "Upgrade King Attack": {},
                        "Upgrade King Spell": {},
                        "Upgrade King Regen": {}
                    }
                
                king_upgrades_per_wave_data = player_data['kingUpgradesPerWave']
                
                for wave, upgrades in enumerate(king_upgrades_per_wave_data, start=1):
                    for upgrade_type in king_upgrades_per_wave_per_type_per_legion[legion].keys():
                        if wave not in king_upgrades_per_wave_per_type_per_legion[legion][upgrade_type]:
                            king_upgrades_per_wave_per_type_per_legion[legion][upgrade_type][wave] = []
                        king_upgrades_per_wave_per_type_per_legion[legion][upgrade_type][wave].append(upgrades.count(upgrade_type))

    for legion, king_upgrades_per_wave_per_type in king_upgrades_per_wave_per_type_per_legion.items():
        waves = list(range(1, max(len(upgrades) for upgrades in king_upgrades_per_wave_per_type.values()) + 1))

        fig = go.Figure()

        for upgrade_type, king_upgrades_per_wave in king_upgrades_per_wave_per_type.items():
            cumulative_upgrades = [0] * len(waves)

            for wave in waves:
                if wave in king_upgrades_per_wave:
                    upgrades = king_upgrades_per_wave[wave]
                    if upgrades:
                        cumulative_upgrades[wave - 1] = cumulative_upgrades[wave - 2] + (sum(upgrades) / len(upgrades))
                    else:
                        cumulative_upgrades[wave - 1] = cumulative_upgrades[wave - 2]
                else:
                    cumulative_upgrades[wave - 1] = cumulative_upgrades[wave - 2]

            fig.add_trace(go.Scatter(x=waves, y=cumulative_upgrades, mode='lines+markers', name=upgrade_type))

        fig.update_layout(
            title=f'Average Cumulative King Upgrades per Wave per Type - {legion}',
            xaxis_title='Wave',
            yaxis_title='Average Cumulative King Upgrades'
        )

        st.plotly_chart(fig)


# Streamlit app
st.title("Average King Upgrades per Wave")

# Specify the directory where the match files are located
match_directory = "data/match_data"

# Get the list of match files
match_files = [f"{match_directory}/{file}" for file in os.listdir(match_directory) if file.endswith('.json')]

if match_files:
    #plot_average_king_upgrades_per_wave(match_files)
    plot_average_cumulative_king_upgrades_per_wave_per_type(match_files)
    plot_average_cumulative_king_upgrades_per_wave_per_type_per_legion(match_files)
else:
    st.warning("No match files found in the specified directory.")
