from dataclasses import dataclass, field
from typing import List


@dataclass
class ClientConfig:
    file_path_map_supergenres: str = field(default_factory=str)
    years_to_search: List[str] = field(default_factory=list)
    tracks_to_search: List[str] = field(default_factory=list)
    number_tracks_per_genre: int = field(default_factory=int)
    market_searched: str = field(default_factory=str)

    supergenre_dictionary: dict = field(init=False)

    def __post_init__(self):
        self.supergenre_dictionary = self.__create_supergenre_mapping()

    def __create_supergenre_mapping(self) -> dict:
        genre_mapping_file = open(self.file_path_map_supergenres,"r")
        genre_mapping_file.readline()

        supergenre_dictionary = {}

        for line in genre_mapping_file:
            line = line.replace('\n','').split(',')
            genre,supergenre = line
            supergenre_dictionary[genre] = supergenre

        return supergenre_dictionary