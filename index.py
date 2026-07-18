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

def get_new_release():
    try:
        token = access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        param = {

            "limit": 50
        }

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params=param
        )

        if response.status_code == 200:
            # print(response.json())
            data = response.json()
            albums = data['albums']['items']
            for i in albums:
                    a = {
                        "album_name": i["name"],
                        "release_date": i["release_date"]
                }
        print(a)
    except Exception as e:
        print ("Error in latest release data fetching..",e)

get_new_release()

# get_albums()