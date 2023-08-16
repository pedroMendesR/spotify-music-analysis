from typing import List

import numpy as np

from ..database.driver import DatabaseDriver


class DataManager:
    similarity_threshold: float
    driver: DatabaseDriver
    managed_genres: List[str]

    def __init__(
        self,
        driver: DatabaseDriver,
        similarity_threshold: float,
        managed_genres: List[str],
    ) -> None:
        self.similarity_threshold = similarity_threshold
        self.driver = driver
        self.managed_genres = managed_genres

    def get_possible_duplicated_tracks(
        self, track_name: str, track_id: str, genre: str
    ):
        query = f'MATCH (t: Track)-[:HAS_GENRE]->(g: Genre {{ name: "{genre}" }}) \
                 WHERE t.name CONTAINS "{track_name}" \
                 AND t.id <> "{track_id}" \
                 RETURN t ORDER BY t.popularity'

        nodes = self.driver.exec(query)

        if len(nodes) > 0:
            return nodes
        return False

    def check_dupe_tracks(self):
        print()
        dupe_tracks_deleted = 0
        for genre in self.managed_genres:
            dupe_tracks_deleted_genre = 0
            all_tracks_nodes = self.driver.exec(
                f"MATCH(t: Track)-[:HAS_GENRE]->(g {{ name: '{genre}' }}) RETURN t"
            )

            for node in all_tracks_nodes:
                node_name, node_id = node["t"]["name"], node["t"]["id"]
                similar_tracks = self.get_possible_duplicated_tracks(
                    node_name, node_id, genre
                )

                if not similar_tracks:
                    continue

                for similar_node in similar_tracks:
                    similarity = self.compare_tracks_stats(node["t"], similar_node["t"])
                    if similarity <= self.similarity_threshold:
                        deleted_node = (
                            node
                            if node["t"]["popularity"] < similar_node["t"]["popularity"]
                            else similar_node
                        )
                        self.remove_duplicate(deleted_node["t"])
                        dupe_tracks_deleted_genre += 1
            print(f"Tracks deletadas em {genre} : {dupe_tracks_deleted_genre}")
            dupe_tracks_deleted += dupe_tracks_deleted_genre
        print(f"\n\nForam excluídas {dupe_tracks_deleted} tracks devido à duplicação.")

    def remove_duplicate(self, node):
        query = f"MATCH(t: Track {{ id: '{node['id']}' }}) DETACH DELETE t"
        self.driver.exec(query)

    def remove_no_features_musics(self):
        query = f"MATCH(t: Track ) WHERE t.valence IS NULL DETACH DELETE t"
        self.driver.exec(query)

    def compare_tracks_stats(self, source, target):
        analysis_values = [
            "loudness",
            "liveness",
            "tempo",
            "valence",
            "instrumentalness",
            "danceability",
            "speechiness",
            "mode",
            "acousticness",
            "energy",
        ]
        attributes_source = np.array([source[key] for key in analysis_values])
        attributes_target = np.array([target[key] for key in analysis_values])

        similarity = np.linalg.norm(attributes_source - attributes_target)
        return similarity
