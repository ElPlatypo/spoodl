import os
import eyed3

from typing import List
from colorama import Fore
from .playlist import Track,Playlist


def scan_library() -> List[Playlist]:
    #get local folder names
    localplaylists = [dir.name for dir in os.scandir("library") if dir.is_dir()]
    librarary = []

    #populate library
    for playlist in localplaylists:
        track_paths = [path for path in os.scandir("library/{}".format(playlist)) if not path.is_dir()]
        tracklist = []
        for path in track_paths:
            track = eyed3.load(path)
            newtrack = Track(title=track.tag.title, artists=str(track.tag.artist).split(","))
            tracklist.append(newtrack)

        newplaylist = Playlist(playlist, tracklist)
        librarary.append(newplaylist)
        print(
            Fore.GREEN + "> Found local playlist: " +
            Fore.WHITE + "{}".format(playlist)
            )
    

    return librarary