from dataclasses import dataclass
from models.Artist import Artist

from models.BaseModel import BaseModel


class Track(BaseModel):
    id: str
    name: str
    popularity: int
    _raw_name: str = "tracks"

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
    raw_name: str = "audio_features"
