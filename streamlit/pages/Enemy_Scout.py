import streamlit as st
import requests

st.title("Legion TD 2 Player Analysis")

player_name = st.text_input("Enter the player's name:")

player_url = f"https://apiv2.legiontd2.com/players/byName/{player_name}"

player_response = requests.get(player_url, headers={'x-api-key': 'vLeBGVkpSH3QAR5M0YVJp8ctyV9Psa4x4Vn0JiYq'})


if player_response.status_code == 200:
    player_data = player_response.json()
    player_id = player_data["_id"]
    print("Got ID")

    # Retrieve player's last 50 matches
    api_url = f"https://apiv2.legiontd2.com/players/matchHistory/{player_id}"
    response = requests.get(api_url, headers={'x-api-key': 'vLeBGVkpSH3QAR5M0YVJp8ctyV9Psa4x4Vn0JiYq'})
    
    if response.status_code == 200:
        matches_data = response.json()
        
        # Filter matches for Normal mode
        normal_matches = [match for match in matches_data if match["queueType"] == "Normal"]
        
        if normal_matches:
            # Analyze legion picks
            legion_picks = {}
            for match in normal_matches:
                player_data = next((p for p in match["playersData"] if p["playerId"] == player_id), None)
                if player_data:
                    legion = player_data["legion"]
                    if legion in legion_picks:
                        legion_picks[legion] += 1
                    else:
                        legion_picks[legion] = 1
            
            st.subheader("Legion Picks")
            for legion, count in legion_picks.items():
                st.write(f"{legion}: {count}")
            
            # Analyze economy
            income_per_wave = []
            workers_per_wave = []
            for match in normal_matches:
                player_data = next((p for p in match["playersData"] if p["playerId"] == player_name), None)
                if player_data:
                    income_per_wave.append(player_data["income_per_wave"])
                    workers_per_wave.append(player_data["workers_per_wave"])
            
            avg_income_per_wave = [sum(wave) / len(wave) for wave in zip(*income_per_wave)]
            avg_workers_per_wave = [sum(wave) / len(wave) for wave in zip(*workers_per_wave)]
            
            st.subheader("Economy Analysis")
            st.write("Average Income per Wave:")
            st.line_chart(avg_income_per_wave)
            st.write("Average Workers per Wave:")
            st.line_chart(avg_workers_per_wave)
            
            # Analyze favored units
            unit_counts = {}
            for match in normal_matches:
                player_data = next((p for p in match["playersData"] if p["playerId"] == player_name), None)
                if player_data:
                    for unit in player_data["units"]:
                        if unit in unit_counts:
                            unit_counts[unit] += 1
                        else:
                            unit_counts[unit] = 1
            
            st.subheader("Favored Units")
            sorted_units = sorted(unit_counts.items(), key=lambda x: x[1], reverse=True)
            for unit, count in sorted_units:
                st.write(f"{unit}: {count}")
        
        else:
            st.warning("No Normal matches found for the player.")
    
    else:
        st.error("Failed to retrieve player matches. Please check the player's name.")