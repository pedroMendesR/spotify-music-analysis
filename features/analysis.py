import os

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# from ..lib.client.DataClient import DataClient
# from ..lib.database.driver import DatabaseDriver
from .charts import RadarChart


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
            radar_chart = RadarChart()
            query = f"MATCH(g: Genre {{ name: '{genre}' }})-[:HAS_GENRE]-(t) RETURN t"
            result = self.driver.exec(query)
            if result == []:
                print(
                    f"\n\032[94mSem dados {self.market_searched} - {self.year_searched} -> {genre}.png\033[0m\n"
                )
                continue
            radar_chart._save_metrics_to_dict(result)
            radar_chart._create_metrics_mean_values(len(result))
            df = pd.DataFrame(dict(r=radar_chart.mean_values, theta=radar_chart.theta))

            polar_categories = [
                f"{key} {round(value,2)}"
                for key, value in zip(radar_chart.theta, radar_chart.mean_values)
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

    def generate_popularity_mean_bar_chart(self, save_most_popular: bool = True):
        supergenres = self.client.config.inv_supergenre_dictionary.keys()
        labels = list(supergenres)
        values = []
        mapped_genres_popularity = {}
        mean_dict = {}
        chart_name = (
            "Gênero mais populares" if save_most_popular else "Gêneros menos populares"
        )
        file_name = "most_popular" if save_most_popular else "less_popular"

        for genre in supergenres:
            query = f"MATCH(t: Track)-[:HAS_GENRE]->(g: Genre {{ name: '{genre}' }}) RETURN t"
            result = self.driver.exec(query)

            if result == []:
                print(
                    f"\n\032[94m Sem tracks {self.market_searched} - {self.year_searched} -> {genre}\033[0m]\n"
                )
                continue

            popularities = []
            for node in result:
                popularities.append(node["t"]["popularity"])

            mean = round(sum(popularities) / len(result), 2)
            values.append(mean)
            mapped_genres_popularity[genre] = mean

        values_mean = round(sum(values) / len(values), 2)

        for genre, popularity in mapped_genres_popularity.items():
            if save_most_popular and popularity >= values_mean:
                mean_dict[genre] = popularity
            elif not save_most_popular and popularity <= values_mean:
                mean_dict[genre] = popularity

        labels = list(mean_dict.keys())
        values = list(mean_dict.values())

        fig = go.Figure(data=[go.Bar(x=labels, y=values)])
        fig.update_layout(
            title=f"Média de Popularidade ({chart_name}) - {self.market_searched}/{self.year_searched} (Média de corte: {values_mean})",
            xaxis_title="Genero",
            yaxis_title="Popularidade",
        )

        save_path = f"features/{self.market_searched}/{self.year_searched}/popularity"
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        print(
            f"\n\033[94mExportando {self.market_searched} - {self.year_searched} -> {file_name}.png\033[0m\n"
        )
        fig.write_image(f"{save_path}/{file_name}.png")
