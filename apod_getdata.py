import requests
import json

def get_data(api_key, start_date=None, end_date=None):
    base_url = "https://api.nasa.gov/planetary/apod"
    params = {"api_key": api_key}
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

with open('apikey.txt', 'r') as file:
    api_key = file.read().strip()

start_date = "2024-08-01"
end_date = "2024-08-05"

data = get_data(api_key, start_date, end_date)

print(json.dumps(data, indent=2))
