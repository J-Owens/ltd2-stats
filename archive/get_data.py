import os
import requests
import json

API_URL = 'https://apiv2.legiontd2.com'
FILE_NAME = "game_data.json"
API_KEY = os.environ["LEGION_API_KEY"]


def load_existing_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def fetch_data_from_api():
    response = requests.get(API_URL + '/games?limit=50&includeDetails=true',
                            headers={'x-api-key': API_KEY})
    return response.json()  # Assuming the API returns a JSON list


def main():
    existing_data = load_existing_data()
    new_data = fetch_data_from_api()

    # Create a set of existing game IDs
    existing_ids = {game['_id'] for game in existing_data}
    print(existing_ids)

    # Filter out games that are already in the existing data
    unique_new_data = [game for game in new_data if game['_id'] not in existing_ids]
    print(len(unique_new_data))

    # Append unique new data to existing data
    existing_data.extend(unique_new_data)

    save_data(existing_data)
    print(f"Saved {len(existing_data)} games to {FILE_NAME}")


if __name__ == "__main__":
    main()
