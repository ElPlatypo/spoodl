from typing import List

if __name__ == "__main__":
    import os

    cwd = os.getcwd()

    print("> scanning local and requested playlists")
    #scan local folder for downloaded playlists
    localplaylists = [f.name for f in os.scandir(cwd) if f.is_dir()]

    # scan for wanted playlists to sync
    playlist_urls = []
    with open("playlists.txt") as file:
        playlist_urls = file.readlines()

    from .playlist import lookup_playlist, Playlist

    print("> fetching playlist metadata")
    # query spotify for playlist names and tracks
    playlists : List[Playlist] = []
    for url in playlist_urls:
        playlist = lookup_playlist(url)
        if playlist.name not in localplaylists:
            os.mkdir(playlist.name)
        playlists.append(playlist)

    from .search import get_song_download_url
    from .download import download_all

    #look for youtube links
    for playlist in playlists:
        print(f"> fetching track URLs for playlist {playlist.name}")
        tracks_to_download = []
        for track in playlist.tracks:
            tracks_to_download.append(get_song_download_url(track.query()))
        print("> downloading all tracks")
        download_all(tracks_to_download, playlist.name)

    print("> finished")

#from mutagen.flac import FLAC
#
#audio = FLAC("example.flac")
#audio["title"] = u"An example"
#audio.pprint()
#audio.save()