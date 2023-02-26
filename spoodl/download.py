from typing import List

from yt_dlp import YoutubeDL

AUDIO_OPTIONS = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        'preferredcodec': 'mp3',
    }],
}

def download_all(urls : List[str]):
    with YoutubeDL(AUDIO_OPTIONS) as ydl:
        for url in urls:
            ydl.download(url)

#todo yt-dl of mp3s