import eyed3
import urllib.request

from colorama import Fore
from .playlist import Track


def tag_mp3_file(track: Track, file: str, extended:bool = False):
    mp3file = eyed3.load(file)

    #comment if extended version
    if extended:
        mp3file.tag.comments.set(u"(extended version)")

    #standard tags
    mp3file.tag.title = track.title
    mp3file.tag.artist = ",".join(track.artists)
    mp3file.tag.album = track.album
    mp3file.tag.date = track.date
    if track.bpm != "":
        mp3file.tag.bpm = track.bpm
        mp3file.tag.key = track.key

    #download and embed cover image
    resp = urllib.request.urlopen(track.cover)
    cover = resp.read()
    mp3file.tag.images.set(3, cover, "image/jpeg", u"cover")

    mp3file.tag.save()

    print(
        Fore.GREEN + "> Done processing track: " +
        Fore.WHITE + "{} ".format(track.title) +
        Fore.GREEN + "by: " +
        Fore.WHITE + "{}".format(track.artists[0])
        )