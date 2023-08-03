from client.Config import ClientConfig
from client.DataClient import DataClient
from database.driver import DatabaseDriver
from models.Artist import ArtistBasicInfo

client_config = ClientConfig()
client = DataClient(config=client_config)
database_driver = DatabaseDriver("neo4j")


def request_artist_basic_info(id_artist: str = None) -> ArtistBasicInfo:
    search_id = client_config.initial_artist_id if not id_artist else id_artist
    data = client.get(f"/artists/{search_id}")
    data["followers"] = data["followers"]["total"]

    del data["external_urls"]
    del data["images"]

    return ArtistBasicInfo(**data)


def run():
    initial_artist = request_artist_basic_info()
    database_driver.exec(f"CREATE (a: Artist {initial_artist.to_cypher()})")
