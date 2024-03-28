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


# Streamlit app
st.title("Average King Upgrades per Wave")

# Specify the directory where the match files are located
match_directory = "data/match_data"

# Get the list of match files
match_files = [f"{match_directory}/{file}" for file in os.listdir(match_directory) if file.endswith('.json')]

if match_files:
    plot_average_king_upgrades_per_wave(match_files)
    plot_average_king_upgrades_per_wave_per_legion(match_files)
else:
    st.warning("No match files found in the specified directory.")
