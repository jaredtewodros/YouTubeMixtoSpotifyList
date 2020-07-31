# Jared Tewodros
# jmt5rg

# import youtube_dl
#
# # use youtube_dl to collect the song name & artist name
# youtube_url = "https://www.youtube.com/watch?v=Ri7-vnrJD3k"
#
# video = youtube_dl.YoutubeDL({}).extract_info(
# youtube_url, download=False)
# song_name = video["track"]
# artist = video["artist"]
# print(song_name)
# print(artist)

def smash(a, b):
    if (a <= b):
        if (b % a == 0):
            print(a)
            smash(a, b/a)
        else:
            a+=3
            smash(a, b)

smash(2, 121)