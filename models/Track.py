from models.BaseModel import BaseModel


class Track(BaseModel):
    id: str
    name: str
    popularity: int
    _raw_name: str = "tracks"
    _node_name: str = "Track"

    def __repr__(self):
        return self.id + "  " + self.name + "  " + self.popularity


class AudioFeature(BaseModel):
    acousticness: float
    danceability: float
    duration_ms: int
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    valence: float
    raw_name: str = "audio_features"
