from typing import List
from client.DataClient import DataClient
from database.driver import DatabaseDriver
from models import BaseModel, Genre, Track
from models.Artist import ArtistBasicInfo


def get_all_requests_and_persist(node_type:BaseModel, edge_to: BaseModel):

    def get_all_requests(func_request):
        def wrapper_get_all_requests(*args, **kwargs):
            #print(*args)
            #print(**kwargs)
            data = func_request(*args, **kwargs)
            print(data)
        return wrapper_get_all_requests
    return get_all_requests

@get_all_requests_and_persist(node_type=Track, edge_to=Genre)
def request_search(client: DataClient, genre:str, year:str=None, market:str="BR",type_content_searched:str="track", limit:int=40, offset:int=0):
    string_search = f"genre: {genre}{' year: '+ year if year is not None else ''}"
    content_type = type_content_searched

    request_string = f"/search?q={string_search}&type={content_type}&market={market}&limit={limit}&offset={offset}"

    print(request_search)
    print("aaa")
    data = client.get(request_string)

    return data

def persist_node():
    pass

def populate_database_v1(client):
    '''
    Função para popular banco de dados orientado a grafos onde:
        - Nós são GENRE_ANO e MUSICA
        - Arestas são top K MUSICAs que apareceram na busca textual do gênero X e ano Y
    '''
    years_to_search = client.config.years_to_search

    for year in years_to_search:
        genres_to_search = list(client.config.supergenre_dictionary.keys())
        
        for genre in genres_to_search:
            pass


def run(client:DataClient, database_driver:DatabaseDriver):
    #populate_database_v1(client)
    #request_search()
    request_search(client=client, genre="rock", limit=2)
    