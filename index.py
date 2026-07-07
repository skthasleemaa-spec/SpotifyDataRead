import base64
import requests
from dotenv import load_dotenv
import os

load_dotenv('.env')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Generate Spotify Access Token
def access_token():
    try:
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()

        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={
                "Authorization": f"Basic {encoded_credentials}"
            },
            data={
                "grant_type": "client_credentials"
            }
        )

        response.raise_for_status()

        print("Token Generated Successfully...")
        return response.json()["access_token"]

    except Exception as e:
        print("Error:", e)


# Search albums (replacement for new releases)
import requests

def get_albums():
    try:
        token = access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {
            "q": "year:2026",
            "type": "album",
            "limit": 10
        }

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params=params
        )

        print(response.status_code)

        if response.status_code == 200:
            print(response.json())
            data = response.json()
            albums = data['albums']['items']
            for i in albums:
                a = {
                    'album_names':i ['name'],
                    'Release _date' : i['release_date']

                }
                print(a)
    except Exception as e:
        print ("Error in latest release data fetching..",e)
        # else:
        #     print(response.json())

get_albums()