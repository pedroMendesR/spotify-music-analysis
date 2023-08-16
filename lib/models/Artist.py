from dataclasses import dataclass
from typing import List

from .BaseModel import BaseModel


@dataclass
class Artist(BaseModel):
    id: str
    spotify_url: str
    name: str
    followers: int
    genres: List[str]
    popularity: int


@dataclass
class ArtistBasicInfo(BaseModel):
    followers: int
    genres: List[str]
    href: str
    id: str
    name: str
    popularity: int
    type: str
    uri: str
