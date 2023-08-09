import pandas as pd

from client.DataClient import DataClient
from database.driver import DatabaseDriver


def request_search():
    pass


def create_supergenres_nodes(driver: DatabaseDriver):
    genres_df = pd.read_csv("extra/mapped_supergenres.csv")
    supergenres = genres_df["supergenre"].unique()

    for genre in supergenres:
        driver.exec(f"CREATE (g: Genre {{ name: '{genre}' }})")


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
    create_supergenres_nodes(database_driver)
    # populate_database_v1(client)
