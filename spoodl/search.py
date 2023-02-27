import re

from youtubesearchpython import VideosSearch

def get_song_download_url(query:str, pattern:str) -> dict:
    original_video = VideosSearch(query, limit = 1)
    extended_video = VideosSearch(query + " extended", limit = 5)
    urls = []
    for url in extended_video.result()["result"]:
        if re.match(pattern, url["title"], re.I):
            urls.append(url["link"])
            
    res = {"original": original_video.result()["result"][0]["link"], "extended": urls}  
    return res