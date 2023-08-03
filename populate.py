from typing import List
from neo4j import Driver, GraphDatabase
from enum import Enum
from util import object_to_cypher_structure
import requests

from classes import Artist, Content

class DataGetter():

    def __init__(self,\
                  api_authorization:str,\
                      api_url:str="https://api.spotify.com/v1",\
                          db_protocol:str="bolt",\
                              db_host:str="localhost",\
                                  db_port: str|int="7687",\
                                      db_auth: tuple[str]=("neo4j", "admin123")) -> None:
        self.api_url = api_url
        self.headers = {"Authorization":api_authorization}
        self.db_url = f"{db_protocol}://{db_host}:{db_port}"
        self.db_auth = db_auth
        self.driver = GraphDatabase.driver(self.db_url, auth=self.db_auth)
        self.max_artists_inserted = 20
        self.artists_id_to_search:List[str] = []
        self.albums_to_search:List[str] = []
        self.tracks_to_search = []

    def set_initial_parameters(self,\
                                id_initial_artist_search: str = "6l3HvQ5sa6mXTsMTB19rO5",\
                                      max_artists_inserted:int=20):
        self.artists_id_to_search.append(id_initial_artist_search)
        self.max_artists_inserted = max_artists_inserted

    def populate_database(self):

        while self.artists_id_to_search != []:

            artist_id = self.artists_id_to_search.pop(0)
            data = self._request_artist_basic_info(artist_id)

            artist = Artist(spotify_url=data["external_urls"]["spotify"],\
                            id=artist_id,\
                            name=data["name"],\
                            followers=data["followers"]["total"],\
                            genres=data["genres"],\
                            popularity=data["popularity"])
            
            self._create_node("Artist", object_to_cypher_structure(artist))



        print("O banco está populado!")

    def _request_artist_basic_info(self, id_artist: str):

        request_string = f"{self.api_url}/artists/{id_artist}"
        response = requests.get(request_string, headers=self.headers)

        data = response.json()
        return data

    def request_albums(self, include_groups:List[str]=["album"], market:str="", limit:int=50, offset:int=0):
        
        groups = ','.join(include_groups)
        market = '&market='+market if market!='' else ''
        request_string = f"{self.api_url}/artists/{self.id}/albums?include_groups={include_groups}{market}&limit={limit}&offet={offset}"

    def _create_node(self, label: str, data: str, alias:str=None):

        with self.driver.session() as session:
            result = session.run(f"CREATE ({alias}:{label} {data})")
            print(result.data.properties)
            return result

"""
# Conectando-se ao banco de dados
uri = "bolt://localhost:7687"  # Verifique o endereço e a porta do seu banco de dados Neo4j
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin123"))

# Executando uma consulta Cypher
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n")

    for record in result:
        print(record)
"""