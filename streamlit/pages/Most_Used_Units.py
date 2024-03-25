import json
from collections import defaultdict
import os
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Most Used Units by Legion", layout="wide")

st.markdown("# Most Used Units by Legion")

def most_used_units_by_legion(match_files):
    total_unit_count = defaultdict(int)
    total_units = 0
    legion_unit_counts = defaultdict(lambda: defaultdict(int))
    legion_total_units = defaultdict(int)
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                legion = player_data['legion']
                for unit in player_data['buildPerWave'][-1]:
                    unit_id = unit.split(':')[0][:-8]
                    total_unit_count[unit_id] += 1
                    total_units +=1
                    legion_unit_counts[legion][unit_id] += 1
                    legion_total_units[legion] += 1
    
    charts = []

    # Total units chart
    sorted_total_units = sorted(total_unit_count.items(), key=lambda x: x[1])
    total_unit_ids = [unit_id for unit_id, _ in sorted_total_units]
    total_counts = [count for _, count in sorted_total_units]
    total_percentages = [count / total_units * 100 for count in total_counts]

    total_chart_data = {
        'Unit ID': total_unit_ids,
        'Count': total_counts,
        'Percentage': total_percentages
    }

    chart = px.bar(total_chart_data, x='Percentage', y='Unit ID', hover_data=['Count'], orientation='h')
    chart.update_layout(title="Most Used Units")
    num_units = len(total_unit_ids)
    chart_height = num_units * 20  # Adjust the multiplier as needed
    chart.update_layout(width=800, height=chart_height)
    charts.append(chart)

    for legion, unit_counts in legion_unit_counts.items():
        sorted_units = sorted(unit_counts.items(), key=lambda x: x[1])
        total_units = legion_total_units[legion]
        unit_ids = [unit_id for unit_id, _ in sorted_units]
        counts = [count for _, count in sorted_units]
        percentages = [count / total_units * 100 for count in counts]
        
        chart_data = {
            'Unit ID': unit_ids,
            'Count': counts,
            'Percentage': percentages
        }
        
        chart = px.bar(chart_data, x='Percentage', y='Unit ID', hover_data=['Count'], orientation='h')
        chart.update_layout(title=f"{legion} Most Used Units")
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
    charts = most_used_units_by_legion(match_files)

    for chart in charts:
        st.plotly_chart(chart)
else:
    st.warning("No match files found in the specified directory.")