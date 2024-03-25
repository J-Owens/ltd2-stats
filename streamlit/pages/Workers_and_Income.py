import json
from collections import defaultdict
import os
import streamlit as st
import plotly.graph_objects as go

def average_workers_and_income_per_wave(match_files):
    worker_counts = defaultdict(list)
    incomes = defaultdict(list)

    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                for wave, workers in enumerate(player_data['workersPerWave'], 1):
                    worker_counts[wave].append(workers)
                for wave, income in enumerate(player_data['incomePerWave'], 1):
                    incomes[wave].append(income)

    waves = list(range(1, len(worker_counts) + 1))
    avg_workers = [sum(worker_counts[wave]) / len(worker_counts[wave]) for wave in waves]
    avg_income = [sum(incomes[wave]) / len(incomes[wave]) for wave in waves]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=waves,
        y=avg_workers,
        name='Avg. Workers',
        mode='lines',
        line=dict(color='dodgerblue')
    ))

    fig.add_trace(go.Scatter(
        x=waves,
        y=avg_income,
        name='Avg. Income',
        mode='lines',
        line=dict(color='lightyellow'),
        yaxis='y2'
    ))

    fig.update_layout(
        title='Average Workers and Income per Wave',
        xaxis_title='Wave',
        yaxis=dict(
            title='Avg. Workers',
            titlefont=dict(color='dodgerblue'),
            tickfont=dict(color='dodgerblue')
        ),
        yaxis2=dict(
            title='Avg. Income',
            titlefont=dict(color='lightyellow'),
            tickfont=dict(color='lightyellow'),
            overlaying='y',
            side='right'
        )
    )

    fig.update_layout(width=1050, height=600)

    st.plotly_chart(fig)

st.title("Average Workers and Income")

# Specify the directory where the match files are located
match_directory = "data/match_data"

# Get the list of match files
match_files = [f"{match_directory}/{file}" for file in os.listdir(match_directory) if file.endswith('.json')]

if match_files:
    average_workers_and_income_per_wave(match_files)
else:
    st.warning("No match files found in the specified directory.")