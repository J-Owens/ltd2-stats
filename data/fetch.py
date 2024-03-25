import os
import json
import requests

# API endpoint URL
api_url = 'https://apiv2.legiontd2.com/games'

# Directory to store the JSON files
data_directory = 'data/match_data'

def match_exists(match_id):
    file_path = os.path.join(data_directory, f'{match_id}.json')
    return os.path.exists(file_path)


def fetch_and_store_matches():
    offset = 0
    limit = 10000
    
    while True:
        params = {
            'limit': 50,
            'offset': offset,
            'sortBy': 'date',
            'sortDirection': -1,
            'includeDetails': 'true',
            'queueType' : 'Normal',
        }
        
        response = requests.get(api_url, params=params, headers={'x-api-key': API_KEY})
        matches = json.loads(response.text)
        
        # Create the data directory if it doesn't exist
        os.makedirs(data_directory, exist_ok=True)
        
        stored_count = 0
        # Save each match as a separate JSON file
        for match in matches:
            game_elo = match.get('gameElo')
            if game_elo >= 2000: # Check if Elo is above threshold
                match_id = match.get('_id')
                if not match_exists(match_id):
                    file_path = os.path.join(data_directory, f'{match_id}.json')
                    with open(file_path, 'w') as file:
                        json.dump(match, file)
                        stored_count += 1
                else:
                    print(f"Match {match_id} already stored.")
        
        print(f"Stored {stored_count} from request")

        offset += 50
        
        if limit <= offset:
            break

fetch_and_store_matches()