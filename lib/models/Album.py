from dataclasses import dataclass
from typing import List

from .BaseModel import BaseModel


@dataclass
class Album(BaseModel):
    id: str
    name: str
    album_type: str
    total_tracks: int
    available_markets: List[str]
    release_date: str
    release_date_precision: str
    spotify_url: str
    album_group: str
