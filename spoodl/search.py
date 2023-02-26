from youtubesearchpython import VideosSearch

# TODO find better name which is as descriptive but shorter
def get_song_download_url(query:str, extended:bool=False) -> str:
    videosSearch = VideosSearch(query, limit = 1)
    return videosSearch.result()["result"][0]["link"]