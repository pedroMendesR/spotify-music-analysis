from typing import List
from neo4j import GraphDatabase
from enum import Enum
import requests


authorization = "Bearer "
headers = {"Authorization":authorization}

id_artista_inicial = "6l3HvQ5sa6mXTsMTB19rO5"
k_profundidade_max = 5

albums_to_search = []
artists_to_search = [id_artista_inicial]


class DataGetter():

    def __init__(self,\
                  api_authorization:str,\
                      api_url:str="https://api.spotify.com/v1/",\
                          db_protocol:str="bolt",\
                              db_host:str="localhost",\
                                  db_port: str|int="7687",\
                                      db_auth: tuple[str]=("neo4j", "admin123")) -> None:
        self.api_url = api_url
        self.headers = {"Authorization":api_authorization}
        self.db_url = f"{db_protocol}://{db_host}:{db_port}"
        self.driver = GraphDatabase.driver(self.db_url, auth=db_auth)

    def _artist_request(id:str, include_groups:List[str]=["album"], market:str="", limit:int=50, offset:int=0):
        
        global albums_to_search

        request_string = f"https://api.spotify.com/v1/artists/{id}/albums?include_groups={','.join(include_groups)}{'&market='+market if market!='' else ''}&limit={limit}&offset={offset}"

        request_json = requests.get(request_string, headers=headers).json()
        
        data = request_json["items"]
        id_albums = [item["id"] for item in data]
        
        albums_to_search = list(set(id_albums+albums_to_search))

        return request_json["total"]<=request_json["limit"] 

print(_artist_request(id_artista_inicial))


#def _album_request(id:str, market:str="", limit:int=50, offset:int=0):



# Conectando-se ao banco de dados
uri = "bolt://localhost:7687"  # Verifique o endereço e a porta do seu banco de dados Neo4j
driver = GraphDatabase.driver(uri, auth=("neo4j", "admin123"))

# Executando uma consulta Cypher
with driver.session() as session:
    result = session.run("MATCH (n) RETURN n")

    for record in result:
        print(record)
