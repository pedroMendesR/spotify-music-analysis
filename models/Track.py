from dataclasses import dataclass

from models.BaseModel import BaseModel


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
    type: str
    id: str
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int

    # def __init__(self, **kwargs) -> None:
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)

    # def _to_cypher_structure():
    #     pass
