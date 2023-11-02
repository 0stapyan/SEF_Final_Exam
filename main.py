import requests
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

def fetch_user_data(offset):
    url = f'https://sef.podkolzin.consulting/api/users/lastSeen?offset={offset}'
    response = requests.get(url)

    if response.status_code == 200:
        users_data = response.json()
        return users_data.get('data', [])
    else:
        print(f"Failed to fetch user data. Status code: {response.status_code}")
        return None


@app.get('/api/users/list')
def get_user_list():
    offset = 0
    users_data = fetch_user_data(offset)

    if users_data is None:
        return []

    print("DEBUG: First user data:", users_data[0] if users_data else "No data")

    users_list = []
    for user in users_data:
        first_seen_timestamp = user.get('firstSeen', None)
        first_seen_str = (
            datetime.utcfromtimestamp(first_seen_timestamp).strftime('%Y-%m-%d %H:%M:%S')
            if first_seen_timestamp is not None else "Unknown"
        )
        users_list.append({
            "username": user.get('nickname', 'Unknown'),
            "userId": user.get('userId', 'Unknown'),
            "firstSeen": first_seen_str
        })

    return users_list

print(get_user_list())
