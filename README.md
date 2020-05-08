# YouTubeMixToSpotifyList
prompts user for a Youtube playlist and transfers those songs to a Spotify playlist, either new or existing

# YouTubeMixToSpotifyList
As someone who shares a Spotify account, deciding who gets to listen when can be a tricky ordeal; especially when people start cutting each other off of the app. To make ends meet, I venture to the vast collection of live and recorded music on YouTube as a change of pace. It turns out that I use YouTube for music so often that over quarentine, I noticed how many songs I actually had in all my playlists. Instead of manually transferring them all over to Spotify, forcing myself to repeatedly do so in the future, I thought it'd be convenient to have a project that would add new YT discoveries into a playlist on my Spotify account, and update it when I found new songs.

# Technologies
Youtube Data API
Youtube DL API
Spotify Web API

# Set Up
link-to-instructions

# Code Examples

# Bugs/Warnings
1. the Spotify authorization token expires about every hour, similar to the login for any other online account, so make sure to refresh often
2. "ERROR: No video formats found; please report this issue on https://yt-dl.org/bug. Make sure you are using the latest version;"
  I think it's a caching issue after not loading any videos from a playlist using Youtube DL's extraction in a while, but still haven't been able to be pin point this bug. I checked that all the video links still existed, and my Youtube-DL version was up to date. However, upon rerunning the program, the bug disappears (which is why I think it has to do with caching).

# To-Do
1. Make REST API
2. Integrate to a web interface



