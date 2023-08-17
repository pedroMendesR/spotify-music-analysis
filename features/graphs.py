class RadarMap:
    theta: list[str] = [
        "liveness",
        "valence",
        "instrumentalness",
        "danceability",
        "speechiness",
        "acousticness",
        "energy",
    ]
    values: dict["str", "float"] = {}
    mean_values: list[float] = []

    def __init__(self):
        self.values = {}
        self.mean_values = []
        for metric in self.theta:
            self.values[metric] = 0.0

    def __str__(self):
        return str(self.theta) + "\n" + str(self.values) + "\n" + str(self.mean_values)

    def _save_metrics_to_dict(self, list_raw_dict: list):
        for item in list_raw_dict:
            for metric in self.theta:
                self.values[metric] += float(item["t"][metric])

    def _create_metrics_mean_values(self, raw_total_items: int):
        for metric in self.theta:
            self.mean_values.append(self.values[metric] / raw_total_items)
