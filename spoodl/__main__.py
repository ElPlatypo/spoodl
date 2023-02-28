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


    # query spotify for playlist names and tracks and make local folder if missing
    print(Fore.CYAN + "> Fetching playlist metadata")

    cloud_library : List[Playlist] = []
    for url in sync_playlist_urls:
        playlist = lookup_playlist(url)
        if not any(playlist.name == local_playlist.name for local_playlist in local_library):
            os.mkdir("library/{}".format(playlist.name))
        cloud_library.append(playlist)
    
    #prompt to delete removed tracks from cloud playlist
    def remove_track(path, title):
        os.remove(path)
        print(
            Fore.CYAN + "> Track: " +
            Fore.WHITE + title +
            Fore.RED + " DELETED " + Fore.WHITE
        )
    yesall = False
    noall = False
    for local_playlist in local_library:
        cloud_playlist = [x for x in cloud_library if x.name == local_playlist.name]
        if cloud_playlist != []:
            for local_track in local_playlist.tracks:
                    if not any(local_track.title == cloud_track.title for cloud_track in cloud_playlist[0].tracks):
                        if yesall == False and noall == False:
                            response = input(
                                Fore.YELLOW + "> Track: " +
                                Fore.WHITE + local_track.title +
                                Fore.YELLOW + " not found in cloud playlist, do you want to " +
                                Fore.RED + "DELETE " +
                                Fore.YELLOW + "it? (y/n) or (Y/N) for all tracks \n> " + Fore.WHITE
                            )
                            if response == "y" or "yes":
                                remove_track(local_track.localpath,local_track.title)
                            elif response == "Y" or "YES":
                                remove_track(local_track.localpath,local_track.title)
                                yesall = True
                            elif response == "N" or "NO":
                                noall = True
                        elif yesall == True:
                            remove_track(local_track.localpath,local_track.title)

                    

    #download one playlist at a time
    for cloud_playlist in cloud_library:
        print(Fore.CYAN + "> Downloading playlist: {}".format(cloud_playlist.name))

        #look for correspondig local library and pass it to download function
        update_playlist = None
        for local_playlist in local_library:
            if local_playlist.name == cloud_playlist.name:
                update_playlist = local_playlist
        download_all(cloud_playlist, update_playlist)


    print(Fore.GREEN + "> Finished")

