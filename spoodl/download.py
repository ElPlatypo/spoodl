from typing import List

from yt_dlp import YoutubeDL

def download_all(urls : List[str], playlist_name: str):
    AUDIO_OPTIONS = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            'preferredcodec': 'mp3',
        }],
        "paths": {
            "temp": "tmp",
            "home": playlist_name,
        }
    }

    with YoutubeDL(AUDIO_OPTIONS) as ydl:
        for url in urls:
            ydl.download(url)

#todo yt-dl of mp3s