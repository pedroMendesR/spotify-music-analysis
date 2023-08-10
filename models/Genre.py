from dataclasses import dataclass, field
from itertools import count

from models.BaseModel import BaseModel


@dataclass
class Genre(BaseModel):
    id: int = field(default_factory=count().__next__)
    name: str = field(default_factory=str)