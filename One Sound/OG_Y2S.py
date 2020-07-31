# Jared Tewodros
# jmt5rg

# Jared Tewodros
# jmt5rg

import json
import os
import google_auth_oauthlib.flow
from googleapiclient import discovery
import googleapiclient.errors
import requests
import youtube_dl
import urllib.parse

"""Issues to Fix"""
"""
1. what if playlist already exists?
    a) check to see if playlist exists --- CHECK!
    b) if it does, grab that playlist id using target_name --- CHECK!
    c) update playlist --- CHECK!
        a. if song to add is on target playlist, skip it (would help with 50 limit, prolly not adding 50 songs)  --- YAYYY FINALLY GOT!
2. submit to github
3. can only add 50 songs at a time, how to change pages?"""

# try to find out why I couldn't pull from secrets
channel_id = input("What is Your Youtube Account's Channel ID? ")
# is there a way to automate refreshing the token when it expires?
spotify_token = "BQCVXovkHP9BGVjK1ircZNZMBQY7GK5UH-M2ozCUKyBMmBhhbiXlDpTQPDErNM_41XV-uGgksxHe_6bDioYcJt2D4I9-xOXfPOMrm2mCfs1bfPYLQiaRoCF_kJkLvjVkT1aqSQXPFGBg5F5zFlP4kw5DrSb83Yex6xaIoe9Oyp0CqPD7xeB9Q7GrxMas0aMUPgcZdU3d4_88Zh13e5WxSBrUceij0WZMPVzNn2TBKDH4TS0Umjvzg03Ml9l8n7kMEur4aUX3tcj8pKjIpA"
# this would be easy to make a user input
spotify_user_id = "gabrielachi"
target_playlist = input("What Youtube Playlist Do You Want to Add to Spotify? ")
playlist_name = input("What Spotify Playlist Would You Like to Modify (either new or existing)? ")
playlist_desc = input("Provide a Description for Your New Playlist: ")
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
nextPageToken = ""
prevPageToken = ""


class YouTubePlaylist:

    def __init__(self):
        # serves as, and behaves like, a constructor for class (not actually constructor tho)
        # self is similar to "this" keyword in Java
        # runs each time an instance from class is made
        self.spotify_client_id = spotify_user_id
        self.spotify_client_token = spotify_token
        self.youtube_client = self.get_youtube_client()
        self.all_song_info = {}

    # 1. log into Youtube
    def get_youtube_client(self):
        """ Log Into Youtube, Copied from Youtube Data API """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client_secrets.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client

    # 2. grab saved Youtube Mix
    def get_mix(self):
        """grab all playlists from youtube and filter mixes"""
        request = self.youtube_client.playlists().list(
            part="snippet,contentDetails",
            channelId="{}".format(channel_id)
        )

        response = request.execute()

        # print("response:",response)

        target_id = ""
        # find target playlist
        for item in response["items"]:
            curr_title = item["snippet"]["title"]

            if curr_title == target_playlist:
                target_id = item["id"]
                # print(item["id"])
                # print(curr_title)

        # print("Is the bug here:",response)

        # print("target_id:", target_id)
        # now I have target playlist, now need the videos from that list
        target_request = self.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            # channelId="{}".format(channel_id),
            playlistId=target_id,
            maxResults=50
        )

        target_response = target_request.execute()

        # print("Should be all videos in target:", target_response)

        # collect info on each video in playlist
        for item in target_response["items"]:
            video_title = item["snippet"]["title"]
            # print("Video title:", video_title)
            video_id = item["snippet"]["resourceId"]["videoId"]
            youtube_url = "https://www.youtube.com/watch?v={}".format(video_id)
            # youtube_url = "https://www.youtube.com/watch?v={}".format(item["id"])
            # print(item["id"])

            # print("URL:", youtube_url)

            # you dl to collect song info
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)
            print("DL Video:", video)
            song_name = video["track"]
            artist = video["artist"]
            # print("artsit from extraction:", artist)

            if song_name is not None and artist is not None:
                # get rid of spaces to prevent gap in endpoints
                # song_name.replace(" ", "%20")
                # artist.replace(" ", "%20")
                # print("Space replaced song:",song_name)
                # print("Space replaced song:", artist)

                # save important info for songs with no missing info
                self.all_song_info[video_title] = {
                    "youtube_url": youtube_url,
                    "song_name": song_name,
                    "artist": artist,

                    # add uri for easy insertion to playlist
                    "spotify_uri": self.get_spotify_uri(song_name, artist)

                }

    # 3. check to see if given playlist exists in Spotify
    def check_for_playlist(self, playlist_name):
        # check if given playlist already exists
        playlist_id = ""

        # 1. get list of all of user's playlists
        endpoint1 = "https://api.spotify.com/v1/users/{}/playlists".format(spotify_user_id)
        response1 = requests.get(
            endpoint1,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_client_token)
            }
        )

        response_json1 = response1.json()

        # 2. check if playlist_name in list
        for item in response_json1["items"]:
            if item["name"] == playlist_name:
                playlist_id = item["id"]

        return playlist_id

    # 4. update playlist if exists
    def update_playlist(self, playlist_id):
        print("playlist_id:",playlist_id)
        # get uris of all songs already in playlist
        endpoint = "https://api.spotify.com/v1/playlists/{}/tracks?fields=items(track(uri))".format(playlist_id)

        response = requests.get(
            endpoint,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_client_token)
            }
        )

        response_json = response.json()

        curr_list_uris = []

        # loop through existing songs and collect uris (since uris are 100% unique to the song)
        items = response_json["items"]
        for i in range(len(items)):
            # print(items[i]["track"]["uri"])
            curr_list_uris.append(items[i]["track"]["uri"])

        keys_to_remove = []

        # print("type:", type(self.all_song_info))
        for song in self.all_song_info:
            # print("song:", song)
            if self.all_song_info[song]["spotify_uri"] in curr_list_uris:
                # print("uri: ", self.all_song_info[song]["spotify_uri"])
                keys_to_remove.append(song)

        for k in keys_to_remove:
            # print("key to remove:", k)
            del self.all_song_info[k]

    # 5. create playlist in Spotify if doesn't exist
    def create_playlist(self):
        # research json.dumps and why it's used here
        request_body2 = json.dumps({
            "name": playlist_name,
            "description": playlist_desc,
            "public": True
        })

        endpoint2 = "https://api.spotify.com/v1/users/{}/playlists".format(self.spotify_client_id)
        response2 = requests.post(
            endpoint2,
            data=request_body2,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_client_token)
            }
        )

        # why'd she do this, isn't it already a json  --- play around with that
        response_json2 = response2.json()

        # print(self.spotify_client_token)
        # print(response_json)

        # playlist id
        return response_json2["id"]

    # 6. lookup song in Spotify
    def get_spotify_uri(self, song_name, artist):
        # print("song:", song_name)
        # print("artist:", artist)
        endpoint = "https://api.spotify.com/v1/search?query=track%3A{}+artist%3A{}&type=track".format(song_name, artist)
        # print("endpoint:", endpoint)
        urllib.parse.quote_plus(endpoint)
        # print("url-endpoint:", endpoint)
        response = requests.get(
            endpoint,
            headers={
                "Authorization": "Bearer {}".format(self.spotify_client_token),
                "Content-Type": "application/json"
            }
        )

        response_json = response.json()
        # print("song i think in spot:", response_json)
        songs = response_json["tracks"]["items"]

        # only use first song
        return songs[0]["uri"]

    # 7. add song to playlist
    def add_song_to_playlist(self):
        # populate dictionary
        self.get_mix()

        # check to see if spotify playlist already exists
        exists = self.check_for_playlist(playlist_name)

        if exists:
            # go through process of filtering out existing song, thus updating rather than dumping repeats
            self.update_playlist(exists)
            playlist_id = exists
        # create a new playlist if doesn't exist
        else:
            playlist_id = self.create_playlist()

        # collect uris
        uris = [info["spotify_uri"]
                for song, info in self.all_song_info.items()]

        # add all songs to playlist
        request_data = json.dumps(uris)

        # print("Le Musica de Harry Frause:", request_data)

        endpoint = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)

        response = requests.post(
            endpoint,
            data=request_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer {}".format(self.spotify_client_token)
            }
        )

        # print("All Song Info: ", self.all_song_info)

        # check for valid response status
        # if response.status_code != 201:
        #     raise ResponseException(response.status_code)

        response_json = response.json()
        return response_json


if __name__ == '__main__':
    cp = YouTubePlaylist()
    cp.add_song_to_playlist()
    print("Transfer Complete. Enjoy the Music!")