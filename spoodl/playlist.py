import spotipy

from datetime import datetime
from typing import List
from dataclasses import dataclass

from os import environ as env

SPOTIPY = spotipy.Spotify(auth_manager=spotipy.SpotifyOAuth(
    client_id=env.get("CLIENT_ID"),
    client_secret=env.get("CLIENT_SECRET"), 
    redirect_uri=env.get("REDIRECT_URI"),
))

@dataclass
class Track:
    name: str
    artists: List[str]
    album: str = ""
    date: datetime = None
    genre: str = ""
    cover: str = ""

    def query(self) -> str:
        return self.name + " " + str.join(" ", self.artists)

@dataclass
class Playlist:
    name: str
    tracks: List[Track]

def lookup_playlist(playlist: List[str]) -> Playlist:
    name = SPOTIPY.playlist(playlist,"name")["name"]
    playlist_tracks = SPOTIPY.playlist_items(playlist,"items(track(name,artists(name),album))")["items"]
    tracks = []
    for track in playlist_tracks:
        tracks.append(
            Track(
                name=track["track"]["name"],
                artists=[ x["name"] for x in track["track"]["artists"] ],
                album=track["track"]["album"]["name"],
                date=datetime.strptime(track["track"]["album"]["release_date"], "%Y-%m-%d"),
                cover=track["track"]["album"]["images"][1]["url"],
            )
        )
        print(tracks[-1])
    return Playlist(name=name, tracks=tracks)