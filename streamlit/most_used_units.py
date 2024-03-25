import json
from collections import defaultdict
import os
import streamlit as st
import plotly.express as px

def most_used_units_by_legion(match_files):
    legion_unit_counts = defaultdict(lambda: defaultdict(int))
    legion_total_units = defaultdict(int)
    
    for file in match_files:
        with open(file, 'r') as f:
            match_data = json.load(f)
            for player_data in match_data['playersData']:
                legion = player_data['legion']
                for build in player_data['buildPerWave']:
                    for unit in build:
                        unit_id = unit.split(':')[0]
                        legion_unit_counts[legion][unit_id] += 1
                        legion_total_units[legion] += 1
    
    charts = []
    for legion, unit_counts in legion_unit_counts.items():
        sorted_units = sorted(unit_counts.items(), key=lambda x: x[1], reverse=True)
        total_units = legion_total_units[legion]
        unit_ids = [unit_id for unit_id, _ in sorted_units]
        counts = [count for _, count in sorted_units]
        percentages = [count / total_units * 100 for count in counts]
        
        chart_data = {
            'Unit ID': unit_ids,
            'Count': counts,
            'Percentage': percentages
        }
        
        chart = px.bar(chart_data, x='Unit ID', y='Count', hover_data=['Percentage'])
        chart.update_layout(title=f"{legion} Most Used Units")
        charts.append(chart)
    
    return charts

# Streamlit app
def main():
    st.title("Most Used Units by Legion")
    
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


if __name__ == '__main__':
    main()