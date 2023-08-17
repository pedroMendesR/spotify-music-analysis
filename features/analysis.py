from os import getenv
from dotenv import load_dotenv
from neo4j import Driver, GraphDatabase
from neo4j.exceptions import DatabaseError, DriverError
import pandas as pd
import plotly.express as px
import os

class DatabaseDriver:
    driver: Driver
    database: str = "neo4j"

    def __init__(self, driver:Driver, database_name: str) -> None:
        self.driver = driver
        self.database = database_name

    def close(self) -> None:
        self.driver.close()

    def exec(self, query: str):
        try:
            with self.driver.session() as session:
                records = session.run(query)
                return records.data()
        except (DriverError, DatabaseError) as exception:
            print(f"Erro: {exception}")
        finally:
            self.close()
            
load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PROTOCOL = getenv("DB_PROTOCOL")
DB_PORT = getenv("DB_PORT")

CONNECTION_URI = f"{DB_PROTOCOL}://{DB_HOST}:{DB_PORT}"

driver = GraphDatabase.driver(uri=CONNECTION_URI, auth=(DB_USER, DB_PASSWORD))
database = "neo4j"

database_driver = DatabaseDriver(driver, database)

YEAR_TO_SEARCH = getenv("YEAR_TO_SEARCH")
MARKET_SEARCHED = getenv("MARKET_SEARCHED")

class RadarMap:
    theta: list[str] = ["liveness", "valence", "instrumentalness", "danceability", "speechiness", "acousticness", "energy"]
    values: dict["str","float"] = {}
    mean_values: list[float] = []
    
    def __init__(self):
        self.values = {}
        self.mean_values = []
        for metric in self.theta:
            self.values[metric] = 0.0
    
    def __str__(self):
        return str(self.theta) + "\n" + str(self.values) + "\n" + str(self.mean_values)
    
    def _save_metrics_to_dict(self, list_raw_dict:list):
        for item in list_raw_dict:
            for metric in self.theta:
                self.values[metric] += float(item["t"][metric])
            
    def _create_metrics_mean_values(self, raw_total_items:int):
        for metric in self.theta:
            self.mean_values.append(self.values[metric]/raw_total_items)

radar_map = RadarMap()

supergenre_name="pop"

query = f"MATCH(g: Genre {{ name: '{supergenre_name}' }})-[:HAS_GENRE]-(t) RETURN t"
result = database_driver.exec(query)

#print(result)

radar_map._save_metrics_to_dict(result)
radar_map._create_metrics_mean_values(len(result))

#print(radar_map.mean_values)
#print(len(radar_map.theta), "  e  ", len(radar_map.mean_values))


df = pd.DataFrame(dict(r=radar_map.mean_values, theta=radar_map.theta))

polar_categories = [f"{key} {round(value,2)}" for key,value in zip(radar_map.theta,radar_map.mean_values)]


fig = px.line_polar(df, r='r', theta=polar_categories, line_close=True, range_r=[0,1])


if not os.path.exists(f"features/{MARKET_SEARCHED}/{YEAR_TO_SEARCH}/radar"):
    os.mkdir(f"features/{MARKET_SEARCHED}/{YEAR_TO_SEARCH}/radar")

fig.write_image(f"features/{MARKET_SEARCHED}/{YEAR_TO_SEARCH}/radar/{supergenre_name}.png")


#fig.show()
