import os
import requests
import json

API_URL = 'https://apiv2.legiontd2.com'
API_KEY = os.environ["LEGION_API_KEY"]

def fetch_data_from_api(request):
    response = requests.get(API_URL + request,
                            headers={'x-api-key': API_KEY})
    return response.json()  # Assuming the API returns a JSON list


def main():
    data = fetch_data_from_api('/games?limit=50&includeDetails=true')


if __name__ == "__main__":
    main()
