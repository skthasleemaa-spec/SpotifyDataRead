import os
import base64
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


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
        print("✅ Token Generated Successfully...\n")

        return response.json()["access_token"]

    except requests.exceptions.RequestException as e:
        print("Error generating token:", e)
        return None


# Fetch 50 albums
def get_albums():

    token = access_token()

    if not token:
        return

    headers = {
        "Authorization": f"Bearer {token}"
    }

    current_year = datetime.now().year

    albums = []

    # Spotify now allows a maximum limit of 10
    for offset in range(0, 50, 10):

        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers=headers,
            params={
                "q": f"year:{current_year}",
                "type": "album",
                "limit": 10,
                "offset": offset
            }
        )

        print("Request URL:", response.request.url)
        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print(response.text)
            return

        data = response.json()

        albums.extend(data["albums"]["items"])

    print("\n" + "=" * 80)
    print(f"Latest Albums Released in {current_year}")
    print("=" * 80)

    if not albums:
        print("No albums found.")
        return

    for i, album in enumerate(albums, start=1):

        artists = ", ".join(
            artist["name"] for artist in album["artists"]
        )

        print(f"\nAlbum {i}")
        print(f"Album Name   : {album['name']}")
        print(f"Artist       : {artists}")
        print(f"Release Date : {album['release_date']}")
        print(f"Total Tracks : {album['total_tracks']}")
        print(f"Spotify URL  : {album['external_urls']['spotify']}")
        print("-" * 80)


# Run
if __name__ == "__main__":
    get_albums()

  
