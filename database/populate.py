from typing import List

from client.DataClient import DataClient
from database.driver import DatabaseDriver
from models.Artist import ArtistBasicInfo
from models.BaseModel import BaseModel
from models.Genre import Genre
from models.Track import Track


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
        cypher_query = f'MATCH (x:{node._node_name}{{id: "{node.id}"}}) RETURN x'
        result = database_driver.exec(cypher_query)

        node_exists = result != []

        if not node_exists:
            cypher_query = f"CREATE (t:{node._node_name} {node.to_cypher()})"
            database_driver.exec(cypher_query)

    def persist_tracks(edge_to_genre: str = None):
        tracks_to_persist = client.config.tracks_to_search

        for track in tracks_to_persist:
            create_node(track)
        # ver se nó ja existe
        # criar nó
        # ver se aresta já existe
        # criar aresta

        pass

    def populate_database_v1():
        """
        Função para popular banco de dados orientado a grafos onde:
            - Nós são GENRE_ANO e MUSICA
            - Arestas são top K MUSICAs que apareceram na busca textual do gênero X e ano Y
        """
        years_to_search = client.config.years_to_search

        for _ in years_to_search:
            genres_to_search = list(client.config.supergenre_dictionary.keys())

            for index, genre in enumerate(genres_to_search):
                supergenre = client.config.supergenre_dictionary[genre]
                num_genres = client.config.inv_supergenre_dictionary[supergenre]

                max_content = int(TRACKS_PER_GENRE / len(num_genres))
                get_all_requests(
                    request_search,
                    content_buffer=client.config.tracks_to_search,
                    max_content=max_content,
                    node_type=Track,
                )(genre=genre, limit=50, offset=0)

                print(f"{genre} persist tracks")
                persist_tracks()

                client.config.tracks_to_search = []

    populate_database_v1()
    # create_supergenres_nodes(client, database_driver)
    """
    get_all_requests(request_search, \
                     content_buffer=client.config.tracks_to_search, \
                        max_content=10, node_type=Track)(genre="rock", limit=9, offset=0)
  
    #for track in client.config.tracks_to_search:
    #    print(track.to_cypher())"""
