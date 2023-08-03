from dataclasses import dataclass, field
from typing import List


@dataclass
class ClientConfig:
    max_artists_inserted: int = 20
    artists_id_to_search: List[str] = field(default_factory=list)
    albums_to_search: List[str] = field(default_factory=list)
    tracks_to_search: List[str] = field(default_factory=list)
    initial_artist_id: str = "1Xyo4u8uXC1ZmMpatF05PJ"  # The Weeknd
