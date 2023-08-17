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
            fig.update_layout(title=f"Radar ({genre}) - {self.market_searched}/{self.year_searched}")
            fig.write_image(f"{save_path}/{genre}.png")

    def generate_supergenres_stats_box_plot(self, plots_per_image=10, generate_plots=True):

        save_path = f"features/{self.market_searched}/{self.year_searched}/boxplot"
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        supergenres = self.client.config.inv_supergenre_dictionary.keys()

        df_total = pd.DataFrame({"genre":[], "popularity": []})
        df = pd.DataFrame({"genre":[], "popularity": []})
        df_var = pd.DataFrame({"genre":[], "popularity": []})

        last_index = plots_per_image
        image_index = 0

        for index,genre in enumerate(supergenres):
            query = f"MATCH(g: Genre {{ name: '{genre}' }})-[:HAS_GENRE]-(t) RETURN t"
            result = self.driver.exec(query)

            popularities = [item["t"]["popularity"] for item in result]

            df_dict = {"genre":genre, "popularity": popularities}
            df_genre = pd.DataFrame(df_dict)

            df = pd.concat([df, df_genre], ignore_index=True)
            df_total = pd.concat([df_total, df_genre], ignore_index=True)

            genre_var = {"genre":genre, "popularity": [df_genre.var(numeric_only=True)["popularity"]]}

            df_var = pd.concat([df_var, pd.DataFrame(genre_var)], ignore_index=True)


            if ((index%last_index == 0 and index != 0) or index == len(supergenres)-1) and generate_plots:
                image_index += 1

                fig = px.box(df, x="genre", y="popularity", points="all")
                fig.update_layout(title=f"Boxplot - {self.market_searched}/{self.year_searched}")
                fig.write_image(f"{save_path}/boxplot_{image_index}.png")

                df = pd.DataFrame({"genre":[], "popularity": []})

        df_var = df_var.dropna()
        df_var = df_var.sort_values(by="popularity")
        
        max_var_genres = df_var.tail(10)["genre"].to_list()
        max_df = df_total[df_total["genre"].isin(max_var_genres)]

        fig = px.box(max_df, x="genre", y="popularity", points="all")
        fig.update_layout(title=f"Boxplot Variâncias Máximas - {self.market_searched}/{self.year_searched}")
        fig.write_image(f"{save_path}/boxplot_max_var.png")

        min_var_genres = df_var.head(10)["genre"].to_list()
        min_df = df_total[df_total["genre"].isin(min_var_genres)]

        fig = px.box(min_df, x="genre", y="popularity", points="all")
        fig.update_layout(title=f"Boxplot Variâncias Mínimas - {self.market_searched}/{self.year_searched}")
        fig.write_image(f"{save_path}/boxplot_min_var.png")

        


        #print(max_var_genres)