from populate import DataGetter

authorization = ""
headers = {"Authorization":authorization}

data_getter = DataGetter(api_authorization=authorization)
data_getter.set_initial_parameters(max_artists_inserted=10)
data_getter.populate_database()