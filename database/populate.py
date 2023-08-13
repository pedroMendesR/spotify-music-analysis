from typing import List

from client.DataClient import DataClient
from database.driver import DatabaseDriver
from models.BaseModel import BaseModel
from models.Track import AudioFeature, Track


def run(client: DataClient, database_driver: DatabaseDriver):
    TRACKS_PER_GENRE = int(client.config.number_tracks_per_genre)

    def request_search():
        pass

    def create_supergenres_nodes():
        # supergêneros obtidos na criação das configurações do cliente
        supergenres = client.config.inv_supergenre_dictionary

        for supergenre, genres in supergenres.items():
            database_driver.exec(
                f"CREATE (g: Genre {{ name: '{supergenre}', subgenres: {genres} }})"
            )

    def populate_database_v1():
        """
        Função para popular banco de dados orientado a grafos onde:
            - Nós são GENRE_ANO e MUSICA
            - Arestas são top K MUSICAs que apareceram na busca textual do gênero X e ano Y
        """
        years_to_search = client.config.years_to_search

        for year in years_to_search:
            genres_to_search = list(client.config.supergenre_dictionary.keys())

            for genre in genres_to_search:
                pass

    def get_all_requests(
        func_request, content_buffer: list, max_content: int, node_type: BaseModel
    ):
        def wrapper_get_all_requests(*args, **kwargs):
            total_items_available = 1
            total_items_getted = 0

            offset = kwargs.get("offset")
            limit = kwargs.get("limit") if kwargs.get("limit") != 0 else 40

            while total_items_getted < total_items_available:
                # obtém o objeto JSON do item principal do request
                kwargs["limit"] = min(limit, total_items_available - total_items_getted)
                kwargs["offset"] = offset + total_items_getted

                data = func_request(*args, **kwargs)
                data = data[node_type._raw_name]

                total_items_available = min(data["total"], max_content)
                total_items_getted += len(data["items"])

                items = data["items"]

                for item in items:
                    content_buffer.append(node_type(item))

                print(total_items_getted, "/", total_items_available)

        return wrapper_get_all_requests

    def authentication_expirated(func_request):
        def wrapper_authentication_expirated(*args, **kwargs):
            data, status = func_request(*args, **kwargs)
            while status == 401:
                client.update_auth_token(
                    input("O token de autenticação expirou, favor inserir outro:\n")
                )
                data, status = func_request(*args, **kwargs)
            return data

        return wrapper_authentication_expirated

    @authentication_expirated
    def request_search(
        genre: str,
        year: str = None,
        market: str = "BR",
        type_content_searched: str = "track",
        limit: int = 40,
        offset: int = 0,
    ):
        string_search = f"genre: {genre}{' year: '+ year if year is not None else ''}"
        content_type = type_content_searched

        request_string = f"/search?q={string_search}&type={content_type}&market={market}&limit={limit}&offset={offset}"

        data, status = client.get(request_string)

        if status != 200:
            raise Exception(f"\033[91m REQUISIÇÃO FALHOU[{status}]: {data} \033[0m")

        return data, status

    def create_node(node: BaseModel):
        cypher_query = f'MATCH (t:{node._node_name}{{id: "{node.id}"}}) RETURN t'
        result = database_driver.exec(cypher_query)

        node_exists = result != []

        if not node_exists:
            cypher_query = f"CREATE (t:{node._node_name} {node.to_cypher()}) RETURN t"
            node = database_driver.exec(cypher_query)
            print(f"\n\033[92m Created Node {node.__repr__()}")
            return node[0]["t"]

        return result[0]["t"]

    def create_edge(from_id: str, to: str) -> None:
        cypher_query = f"MATCH (n: Track {{ id: '{from_id}' }}) MATCH (g: Genre {{ name: '{to}' }}) CREATE (n)-[:HAS_GENRE]->(g)"
        database_driver.exec(cypher_query)

    def update_track_info(track_id: str, features: dict) -> None:
        set_attr_string = "SET "
        for index, (key, value) in enumerate(features.items()):
            set_attr_string += (
                f"t.{key} = {value}{', ' if index < len(features) - 1 else ';'}"
            )

        cypher_query = f"MATCH (t: Track {{ id: '{track_id}' }}) {set_attr_string}"
        database_driver.exec(cypher_query)

    def map_and_remove_unused_audio_feature(features: List[AudioFeature]) -> dict:
        mapped_features = {}
        for feature in features:
            feature.pop("track_href", None)
            feature.pop("analysis_url", None)
            feature.pop("track_href", None)
            feature.pop("type", None)
            feature.pop("uri", None)
            track_id = feature["id"]
            feature.pop("id", None)
            mapped_features[track_id] = feature
        return mapped_features

    def bulk_persist_track_audio_features(tracks_ids: List[str]) -> None:
        tracks_ids_string = ",".join(tracks_ids)

        data, _ = client.get("/audio-features", {"ids": tracks_ids_string})
        mapped_features = map_and_remove_unused_audio_feature(data["audio_features"])
        for track_id, feature in mapped_features.items():
            update_track_info(track_id, feature)

    def persist_tracks(edge_to_genre: str = None):
        tracks_to_persist = client.config.tracks_to_search
        tracks_ids = []

        for track in tracks_to_persist:
            node = create_node(track)
            create_edge(node["id"], edge_to_genre)
            tracks_ids.append(node["id"])

        bulk_persist_track_audio_features(tracks_ids)

    def populate_database_v1():
        """
        Função para popular banco de dados orientado a grafos onde:
            - Nós são GENRE_ANO e MUSICA
            - Arestas são top K MUSICAs que apareceram na busca textual do gênero X e ano Y
        """
        years_to_search = client.config.years_to_search

        for _ in years_to_search:
            genres_to_search = list(client.config.supergenre_dictionary.keys())

            for _, genre in enumerate(genres_to_search):
                supergenre = client.config.supergenre_dictionary[genre]
                num_genres = client.config.inv_supergenre_dictionary[supergenre]

                max_content = int(TRACKS_PER_GENRE / len(num_genres))
                get_all_requests(
                    request_search,
                    content_buffer=client.config.tracks_to_search,
                    max_content=max_content,
                    node_type=Track,
                )(genre=genre, limit=50, offset=0)

                print(f"\033[92m Persisting \033[94m{genre} \033[0mTracks")
                persist_tracks(supergenre)

                client.config.tracks_to_search = []

    create_supergenres_nodes()
    populate_database_v1()
