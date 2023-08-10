from dataclasses import dataclass, field
from typing import List

import pandas as pd


@dataclass
class ClientConfig:
    file_path_map_supergenres: str = field(default_factory=str)
    years_to_search: List[str] = field(default_factory=list)
    tracks_to_search: List[str] = field(default_factory=list)
    number_tracks_per_genre: int = field(default_factory=int)
    market_searched: str = field(default_factory=str)

    supergenre_dictionary: dict = field(init=False)
    inv_supergenre_dictionary: dict = field(init=False)

    def __post_init__(self):
        self.supergenre_dictionary, self.inv_supergenre_dictionary = self.__create_supergenre_mapping()

    def __create_supergenre_mapping(self) -> dict:
        genres_df = pd.read_csv(self.file_path_map_supergenres)
        supergenre_dictionary = pd.Series(genres_df.supergenre.values, index=genres_df.genre).to_dict()

        super_to_genres = {}

        for genre, supergenre in supergenre_dictionary.items():
            super_to_genres[supergenre] = super_to_genres.get(supergenre, []) + [genre]

        return supergenre_dictionary, super_to_genres