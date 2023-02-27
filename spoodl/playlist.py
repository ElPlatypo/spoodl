import spotipy

from datetime import datetime
from typing import List
from dataclasses import dataclass
from colorama import Fore
from os import environ as env

SPOTIPY = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
    client_id=env.get("CLIENT_ID"),
    client_secret=env.get("CLIENT_SECRET"), 
    redirect_uri=env.get("REDIRECT_URI"),
))

@dataclass
class Track:
    title: str
    artists: List[str]
    album: str = ""
    date: datetime = None
    cover: str = ""
    bpm: str = ""

    def query(self) -> str:
        return self.title + " " + str.join(" ", self.artists)

@dataclass
class Playlist:
    name: str
    tracks: List[Track]

def lookup_playlist(playlist: List[str]) -> Playlist:
    name = SPOTIPY.playlist(playlist,"name")["name"]
    playlist_tracks = SPOTIPY.playlist_items(playlist,"items(track(name,artists(name),album,id))")["items"]
    tracks = []
    for track in playlist_tracks:
        tracks.append(
            Track(
                title=track["track"]["name"],
                artists=[ x["name"] for x in track["track"]["artists"] ],
                album=track["track"]["album"]["name"],
                date=datetime.strptime(track["track"]["album"]["release_date"], "%Y-%m-%d"),
                cover=track["track"]["album"]["images"][1]["url"],
                bpm=int(float(SPOTIPY.audio_analysis(track["track"]["id"])["track"]["tempo"]))
            )
        )
        print(
            Fore.GREEN + "> Found track: " + 
            Fore.WHITE + "{} ".format(track["track"]["name"]) +
            Fore.GREEN + "album: " +
            Fore.WHITE + "{}".format(track["track"]["album"]["name"]))

    return Playlist(name=name, tracks=tracks)