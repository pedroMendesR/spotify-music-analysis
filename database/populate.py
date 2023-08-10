from client.DataClient import DataClient
from database.driver import DatabaseDriver


def request_search():
    pass


def create_supergenres_nodes(client: DataClient, driver: DatabaseDriver):

    # supergêneros obtidos na criação das configurações do cliente
    supergenres = client.config.supergenre_dictionary

    # inverte o mapeamento para {supergênero: List[gênero]}, incluindo também subgeneros no banco
    super_to_genres = {}
    for genre, supergenre in supergenres.items():
        super_to_genres[supergenre] = super_to_genres.get(supergenre, []) + [genre]

    for supergenre,genres in super_to_genres.items():
        driver.exec(f"CREATE (g: Genre {{ name: '{supergenre}', subgenres: {genres} }})")


def populate_database_v1(client):
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


def run(client: DataClient, database_driver: DatabaseDriver):
    create_supergenres_nodes(client, database_driver)
    # populate_database_v1(client)
