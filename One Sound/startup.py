# Jared Tewodros
# jmt5rg

from flask_spotify_auth import getAuth, refreshAuth, getToken
from flask_spotify_auth import getAuth, getToken
import googleapiclient.discovery
import googleapiclient.errors
import requests, json

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

# Add your client ID
CLIENT_ID = "53754c6314ec4175b8dc3d23c864cb5a"

# aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "6677e13f615b4cfda88371b233b9ae08"

# Port and callback url can be changed or ledt to localhost:5000
PORT = "5000"
CALLBACK_URL = "http://localhost"
# CALLBACK_URL = "127.0.0.1"

# Add needed scope from spotify user
# SCOPE = "streaming user-read-birthdate user-read-email user-read-private"
SCOPE = "playlist-modify-public playlist-modify-private user-read-playback-position user-read-private user-read-email playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative user-follow-read user-follow-modify user-read-playback-state user-read-currently-playing user-modify-playback-state user-read-recently-played"
# token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown
TOKEN_DATA = []
SPOTIFY_URL_ID = "https://api.spotify.com/v1/me"


def getSpotUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getChannelId(credentials):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        mine=True
    )
    response = request.execute()
    return response['items'][0]['id']


def getId(spot_client_secret):
    headers = {"Authorization": "Bearer {}".format(spot_client_secret)}
    get = requests.get(SPOTIFY_URL_ID, headers=headers)
    get = get.json()
    return get["id"]


def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
    return TOKEN_DATA[0]


def refreshToken(time):
    global TOKEN_DATA
    time.sleep(time)
    TOKEN_DATA = refreshAuth()


def getAccessToken():
    return TOKEN_DATA