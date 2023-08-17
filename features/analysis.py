import os

import pandas as pd
import plotly.express as px

# from ..lib.client.DataClient import DataClient
# from ..lib.database.driver import DatabaseDriver
from .graphs import RadarMap


class Analysis:
    driver: any
    market_searched: str
    year_searched: str
    client: any

    def __init__(
        self,
        driver: any,
        market_searched: str,
        year_searched: str,
        client: any,
    ) -> None:
        self.driver = driver
        self.market_searched = market_searched
        self.year_searched = year_searched
        self.client = client

    def generate_supergenres_stats_radar_map(self):
        supergenres = self.client.config.inv_supergenre_dictionary.keys()

        for genre in supergenres:
            radar_graph = RadarMap()
            query = f"MATCH(g: Genre {{ name: '{genre}' }})-[:HAS_GENRE]-(t) RETURN t"
            result = self.driver.exec(query)
            if result == []:
                print(
                    f"\n\032[94mSem dados {self.market_searched} - {self.year_searched} -> {genre}.png\033[0m\n"
                )
                continue
            radar_graph._save_metrics_to_dict(result)
            radar_graph._create_metrics_mean_values(len(result))
            df = pd.DataFrame(dict(r=radar_graph.mean_values, theta=radar_graph.theta))

            polar_categories = [
                f"{key} {round(value,2)}"
                for key, value in zip(radar_graph.theta, radar_graph.mean_values)
            ]

            fig = px.line_polar(
                df, r="r", theta=polar_categories, line_close=True, range_r=[0, 1]
            )

            save_path = f"features/{self.market_searched}/{self.year_searched}/radar"
            if not os.path.exists(save_path):
                os.mkdir(save_path)

            print(
                f"\n\033[94mExportando {self.market_searched} - {self.year_searched} -> {genre}.png\033[0m\n"
            )
            fig.write_image(f"{save_path}/{genre}.png")
