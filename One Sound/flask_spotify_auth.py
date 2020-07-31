# Jared Tewodros
# jmt5rg

import base64, json, requests

SPOTIFY_URL_AUTH = 'https://accounts.spotify.com/authorize/?'
SPOTIFY_URL_TOKEN = 'https://accounts.spotify.com/api/token/'
RESPONSE_TYPE = 'code'
HEADER = 'application/x-www-form-urlencoded'
REFRESH_TOKEN = ''
SCOPE = "playlist-modify-public playlist-modify-private user-read-playback-position user-read-private user-read-email playlist-read-private user-library-read user-library-modify user-top-read playlist-read-collaborative user-follow-read user-follow-modify user-read-playback-state user-read-currently-playing user-modify-playback-state user-read-recently-played"


def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id,redirect_uri, scope)                                                          
    return data

# def getBearerToken(client_id, client_secret, redirect_uri):
#     body = {
#         "client_id": client_id,
#         "client_secret": client_secret,
#         "response_type": "token",
#         "redirect_uri": redirect_uri,
#         "scope": SCOPE
#     }
#     # iden = "{}:{}".format(client_id, client_secret)

#     get = requests.get(SPOTIFY_URL_AUTH, params=body)
#     print("HOPE THIS WORKED", get)
#     get = get.json()
#     return get["access_token"]

# def getToken(code, client_id, client_secret, redirect_uri):
#     body = {
#         "client_id": client_id,
#         "response_type": "token",
#         "redirect_uri": redirect_uri,
#         "scope": SCOPE
#         # "client_id": client_id,
#         # "client_secret": client_secret
#     }
#     # client_id = client_id
#     # client_secret = client_secret
#     # iden = "{}:{}".format(client_id, client_secret)
#     # # encoded = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
#     # headers = {"Authorization": "Bearer {}".format(iden)}
#     data = "{}client_id={}&redirect_uri{}scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, SCOPE)
#     # get = requests.get(SPOTIFY_URL_AUTH, params=body)
#     get = requests.get(data).json()
#     print("NFOEWFNEIOFW: ", get)
#     print("LOL WHAAAAAAAAAAAAAAAAAAAAA", get.json())
#     return get.json()

def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code": code,
        "redirect_uri": redirect_uri
        # "client_id": client_id,
        # "client_secret": client_secret
    }
    client_id = client_id
    client_secret = client_secret
    iden = "{}:{}".format(client_id, client_secret)
    encoded = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    headers = {"Content-Type": HEADER, "Authorization": "Basic {}".format(encoded)}

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    return handleToken(json.loads(post.text))


def handleToken(response):
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]


def refreshAuth():
    body = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=HEADER)
    p_back = json.dumps(post_refresh.text)

    return handleToken(p_back)