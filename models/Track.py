from dataclasses import dataclass
from models.Artist import Artist

from models.BaseModel import BaseModel

@dataclass
class Track(BaseModel):
    artist: Artist

@dataclass
class AudioFeature(BaseModel):
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
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int
    type_name: str = "audio_features"
