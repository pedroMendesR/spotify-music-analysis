from os import getenv

from dotenv import load_dotenv

from features.analysis import Analysis
from lib.client.Config import ClientConfig
from lib.client.DataClient import DataClient
from lib.database.driver import DatabaseDriver
from lib.database.populate import run
from lib.manager.DataManager import DataManager

load_dotenv()

SUPERGENRES_MAPPING_PATH = getenv("SUPERGENRES_MAPPING_PATH")
YEAR_TO_SEARCH = [getenv("YEAR_TO_SEARCH")]
NUMBER_TOP_TRACKS_PER_GENRE = getenv("NUMBER_TOP_TRACKS_PER_GENRE")
MARKET_SEARCHED = getenv("MARKET_SEARCHED")

client_config = ClientConfig(
    file_path_map_supergenres=SUPERGENRES_MAPPING_PATH,
    years_to_search=YEAR_TO_SEARCH,
    number_tracks_per_genre=NUMBER_TOP_TRACKS_PER_GENRE,
    market_searched=MARKET_SEARCHED,
)

client = DataClient(config=client_config)
database_driver = DatabaseDriver("neo4j")
data_manager = DataManager(
    database_driver, 5.00, list(client_config.inv_supergenre_dictionary.keys())
)

if __name__ == "__main__":
    # run(client=client, database_driver=database_driver)
    # data_manager.remove_no_features_musics()
    # data_manager.check_dupe_tracks()
    analysis = Analysis(database_driver, MARKET_SEARCHED, YEAR_TO_SEARCH[0], client)
    analysis.generate_supergenres_stats_radar_map()
