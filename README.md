# spoodl
![logo](img/logo.jpg) <br />
(logo courtesy of stable-diffusion)

This Python script allows you to synchronize and download playlists from Spotify using the Spotipy library. It scans your local library, compares it with requested playlists, and downloads missing tracks.

## Prerequisites

- Python 3.x
- Spotipy
- colorama
- yt_dlp
- eyed3

## Installation

1. Install the required Python packages:
  - ```pip install spotipy colorama yt-dlp eyed3```

2. Obtain Spotify API credentials:
  - Go to the Spotify Developer Dashboard.
  - Create a new application and note down the CLIENT_ID, CLIENT_SECRET, and REDIRECT_URI.

3. Create a playlists.txt file:
  - Create a text file named playlists.txt in the same directory as the script.
  - Add the Spotify URLs of the playlists you want to sync, each on a new line.

## Usage

Simply run with:
``` python3 -m spoodl ```

## Features

- Scans local and requested playlists.
- Fetches playlist metadata from Spotify.
- Downloads missing tracks from YouTube.
- Handles extended versions of tracks.
- Embeds metadata and cover images in downloaded MP3 files.


For research pourposes only, use at own risk!
