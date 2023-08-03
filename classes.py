

from ast import List
from enum import Enum

class Artist():

    def __init__(self,\
                  spotify_url:str,\
                      id: str,\
                          name: str,\
                              followers: int,\
                                  genres:list[str],\
                                      popularity: int) -> None:
        self.spotify_url = spotify_url
        self.id = id
        self.name = name
        self.followers = followers
        self.genres = genres
        self.popularity = popularity
    
class Content():

    def __init__(self,\
                  id: str,\
                      name:str,\
                          album_type: str,\
                              total_tracks: int,\
                                  available_markets: list[str],\
                                      release_date: str,\
                                          release_date_precision: str,\
                                              spotify_url:str,\
                                                  album_group: str) -> None:
        self.id = id
        self.name = name
        self.album_type = album_type
        self.total_tracks = total_tracks
        self.available_markets = available_markets
        self.release_date = release_date
        self.release_date_precision = release_date_precision
        self.spotify_url = spotify_url
        self.album_group = album_group

class AudioFeature:
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    type: str
    id: str
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _to_cypher_structure():
        pass