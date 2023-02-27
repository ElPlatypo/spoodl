import eyed3
import urllib.request

from .playlist import Track
from typing import Dict


def tag_mp3_file(track: Track, file: str, extended:bool = False):
    mp3file = eyed3.load(file)

    if extended:
        mp3file.tag.comments.set(u"(extended version)")
    mp3file.tag.title = track.title
    mp3file.tag.artist = ",".join(track.artists)
    mp3file.tag.album = track.album
    mp3file.tag.date = track.date
    mp3file.tag.bpm = track.bpm

    resp = urllib.request.urlopen(track.cover)
    cover = resp.read()
    mp3file.tag.images.set(3, cover, "image/jpeg", u"cover")

    mp3file.tag.save()

    print("> Done processing track: {} by: {}".format(track.title, track.artists))