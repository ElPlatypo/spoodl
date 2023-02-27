import os

from typing import List
from colorama import Fore
from .localscan import scan_library
from .playlist import Playlist, lookup_playlist
from .download import download_all

if __name__ == "__main__":
    
    #get current working dir and crates root library folder
    cwd = os.getcwd()
    if not os.path.exists("library"):
        os.mkdir("library")


    #scan local folder for downloaded playlists amd tracks
    print(Fore.CYAN + "> Scanning local and requested playlists")

    local_library: List[Playlist] = scan_library()


    # scan for wanted playlists to sync
    print(Fore.CYAN + "> Loading playlists.txt")

    sync_playlist_urls = []
    with open("playlists.txt") as file:
        sync_playlist_urls = file.readlines()


    # query spotify for playlist names and tracks
    print(Fore.CYAN + "> Fetching playlist metadata")

    cloud_library : List[Playlist] = []
    for url in sync_playlist_urls:
        playlist = lookup_playlist(url)
        if not any(playlist.name == local_playlist.name for local_playlist in local_library):
            os.mkdir("library/{}".format(playlist.name))
        cloud_library.append(playlist)


    #look for youtube links
    for cloud_playlist in cloud_library:
        print(Fore.CYAN + "> Downloading playlist: {}".format(cloud_playlist.name))

        update_playlist = None
        for local_playlist in local_library:
            if local_playlist.name == cloud_playlist.name:
                update_playlist = local_playlist
        download_all(cloud_playlist, update_playlist)


    print(Fore.GREEN + "> Finished")

