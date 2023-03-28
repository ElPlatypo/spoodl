import os
import shutil

from colorama import Fore
from yt_dlp import YoutubeDL
from .playlist import Playlist
from .search import get_song_download_url
from .postprocess import tag_mp3_file


def download_all(cloud_playlist: Playlist, local_playlist: Playlist):
    AUDIO_OPTIONS = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            'preferredcodec': 'mp3',
        }],
        "paths": {
            "home": "tmp" ,
        },
        "restrictfilenames": "true",
    }

    with YoutubeDL(AUDIO_OPTIONS) as ydl:

        
        for cloud_track in cloud_playlist.tracks:

            #chech if track has already been downloaded
            check = False
            if local_playlist is not None:
                for local_track in local_playlist.tracks:
                    if cloud_track.title == local_track.title and cloud_track.album == cloud_track.album:
                        check = True


            if check == False:
                pattern = "^(?=.*\\b{}\\b)(?=.*\\b{}\\b)(?=.*\\bextended\\b).*$".format(cloud_track.title, cloud_track.artists[0])
                matched_urls = get_song_download_url(cloud_track.query(), pattern)
                skip = False

                #ask user for correct extended version
                if matched_urls["extended"] != [] and skip == False:

                    print(
                        Fore.GREEN + "> Found possible extended versions for track:" +
                        Fore.WHITE + " {}".format(cloud_track.title) +
                        Fore.GREEN + "\n> Please specify wich (if any) to download (0-{})".format(matched_urls["extended"].__len__() + 1)
                        )
                    
                    index = 0
                    for url in matched_urls["extended"]:
                        print(Fore.GREEN + "> ({}) ".format(index) + Fore.WHITE + "{}".format(url))
                        index += 1

                    print(Fore.GREEN + "> ({}) Skip extended version and download original tarck".format(index))
                    index += 1
                    print(Fore.GREEN + "> ({}) Skip extended version and download original for ALL tracks".format(index) + Fore.WHITE)
                    x = False
                    while x == False:
                        selected_url = input(Fore.GREEN + "> " + Fore.WHITE)
                        if float(selected_url).is_integer() and float(selected_url) in range(0, index - 1):
                            ydl.download(matched_urls["extended"][int(selected_url)])
                            tag_mp3_file(cloud_track, os.path.join("tmp", os.listdir("tmp")[0]), True)
                            x = True

                        elif float(selected_url) == index - 1:
                            ydl.download(matched_urls["original"])
                            tag_mp3_file(cloud_track, os.path.join("tmp", os.listdir("tmp")[0]), False)
                            x = True
                        
                        elif float(selected_url) == index:
                            skip == True

                        else:
                            print("> Error reading choice, please select a number between 0-5")

                else:
                    ydl.download(matched_urls["original"])
                    tag_mp3_file(cloud_track, os.path.join("tmp", os.listdir("tmp")[0]), False)
                
                #move file to appropriate folder
                shutil.move(os.path.join("tmp", os.listdir("tmp")[0]), os.path.join("library/{}".format(cloud_playlist.name), cloud_track.title.replace("/","") + "-" + " ".join(cloud_track.artists).replace("/","") + ".mp3"))
            else:
                print(
                    Fore.GREEN + "> " + 
                    Fore.WHITE + "{} ".format(cloud_track.title) +
                    Fore.GREEN + "by: " +
                    Fore.WHITE + "{} ".format(cloud_track.artists[0]) + 
                    Fore.GREEN + "already downloaded, skipping" + Fore.WHITE
                    )

        if os.path.exists("tmp"):
            shutil.rmtree("tmp")