from dataclasses import dataclass, field
from os import getenv
from typing import List

from dotenv import load_dotenv

load_dotenv()

API_SCRAP_HOME = getenv("API_SCRAP_HOME")

@dataclass
class ClientConfig:
    file_path_map_supergenres: str = f"{API_SCRAP_HOME}/extra/default_supergenres_map.csv"
    supergenre_dictionary: dict = field(init=False)
    # Aqui seria útil se colocassemos ranges? Por exemplo, 2018-2021 
    years_to_search: List[str] = field(default_factory=list)
    genres_to_search: List[str] = field(default_factory=list)
    tracks_to_search: List[str] = field(default_factory=list)

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