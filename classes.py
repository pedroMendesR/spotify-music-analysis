

from enum import Enum

class API_Enum(Enum):

    @staticmethod
    def _get_enum(original_name:str) -> "Genre":
        original_name = original_name.upper()
        original_name = original_name.replace("-","_")
        return getattr(Genre, original_name)
    
class Genre(API_Enum):

    ACOUSTIC = 0
    AFROBEAT = 1
    ALT_ROCK = 2
    ALTERNATIVE = 3
    AMBIENT = 4
    ANIME = 5
    BLACK_METAL = 6
    BLUEGRASS = 7
    BLUES = 8
    BOSSANOVA = 9
    BRAZIL = 10
    BREAKBEAT = 11
    BRITISH = 12
    CANTOPOP = 13
    CHICAGO_HOUSE = 14
    CHILDREN = 15
    CHILL = 16
    CLASSICAL = 17
    CLUB = 18
    COMEDY = 19
    COUNTRY = 20
    DANCE = 21
    DANCEHALL = 22
    DEATH_METAL = 23
    DEEP_HOUSE = 24
    DETROIT_TECHNO = 25
    DISCO = 26
    DISNEY = 27
    DRUM_AND_BASS = 28
    DUB = 29
    DUBSTEP = 30
    EDM = 31
    ELECTRO = 32
    ELECTRONIC = 33
    EMO = 34
    FOLK = 35
    FORRO = 36
    FRENCH = 37
    FUNK = 38
    GARAGE = 39
    GERMAN = 40
    GOSPEL = 41
    GOTH = 42
    GRINDCORE = 43
    GROOVE = 44
    GRUNGE = 45
    GUITAR = 46
    HAPPY = 47
    HARD_ROCK = 48
    HARDCORE = 49
    HARDSTYLE = 50
    HEAVY_METAL = 51
    HIP_HOP = 52
    HOLIDAYS = 53
    HONKY_TONK = 54
    HOUSE = 55
    IDM = 56
    INDIAN = 57
    INDIE = 58
    INDIE_POP = 59
    INDUSTRIAL = 60
    IRANIAN = 61
    J_DANCE = 62
    J_IDOL = 63
    J_POP = 64
    J_ROCK = 65
    JAZZ = 66
    K_POP = 67
    KIDS = 68
    LATIN = 69
    LATINO = 70
    MALAY = 71
    MANDOPOP = 72
    METAL = 73
    METAL_MISC = 74
    METALCORE = 75
    MINIMAL_TECHNO = 76
    MOVIES = 77
    MPB = 78
    NEW_AGE = 79
    NEW_RELEASE = 80
    OPERA = 81
    PAGODE = 82
    PARTY = 83
    PHILIPPINES_OPM = 84
    PIANO = 85
    POP = 86
    POP_FILM = 87
    POST_DUBSTEP = 88
    POWER_POP = 89
    PROGRESSIVE_HOUSE = 90
    PSYCH_ROCK = 91
    PUNK = 92
    PUNK_ROCK = 93
    R_N_B = 94
    RAINY_DAY = 95
    REGGAE = 96
    REGGAETON = 97
    ROAD_TRIP = 98
    ROCK = 99
    ROCK_N_ROLL = 100
    ROCKABILLY = 101
    ROMANCE = 102
    SAD = 103
    SALSA = 104
    SAMBA = 105
    SERTANEJO = 106
    SHOW_TUNES = 107
    SINGER_SONGWRITER = 108
    SKA = 109
    SLEEP = 110
    SONGWRITER = 111
    SOUL = 112
    SOUNDTRACKS = 113
    SPANISH = 114
    STUDY = 115
    SUMMER = 116
    SWEDISH = 117
    SYNTH_POP = 118
    TANGO = 119
    TECHNO = 120
    TRANCE = 121
    TRIP_HOP = 122
    TURKISH = 123
    WORK_OUT = 124
    WORLD_MUSIC = 125

class AlbumType(API_Enum):

    ALBUM = 1
    SINGLE = 2
    COMPILATION = 3
    APPEARS_ON = 4

class ReleaseDatePrecision(API_Enum):

    YEAR = 1
    MONTH = 2
    DAY = 3

class Artist():

    def __init__(self,\
                  spotify_url:str,\
                      id: str,\
                          name: str,\
                              followers: int,\
                                  genres:list[str],\
                                      popularity: int) -> None:
        self.spotify_url = spotify_url
        self.id = id
        self.name = name
        self.followers = followers
        self.genres = genres #[Genre._get_enum(genre) for genre in genres]
        self.popularity = popularity
        self.content = []
        self.num_contents = 0
    
class Content():

    def __init__(self,\
                  id: str,\
                      name:str,\
                          album_type: str,\
                              total_tracks: int,\
                                  available_markets: list[str],\
                                      release_date: str,\
                                          release_date_precision: str,\
                                              spotify_url:str,\
                                                  album_group: str) -> None:
        self.id = id
        self.name = name
        self.album_type = album_type #AlbumType._get_enum(album_type)
        self.total_tracks = total_tracks
        self.available_markets = available_markets
        self.release_date = release_date
        self.release_date_precision = release_date_precision #ReleaseDatePrecision._get_enum(release_date_precision)
        self.spotify_url = spotify_url
        self.album_group = album_group #AlbumType._get_enum(album_group)
        self.artists = [Artist("url_artista1","sadas5da","FilipeyDelas",9999999,["pop-samba","pop-bamba"],156165),\
                        Artist("url_artista2","1sa5d1as5","TulinDela",151551,["pop-dark","otaku"],1515)]

class AudioFeature:
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    type: str
    id: str
    uri: str
    track_href: str
    analysis_url: str
    duration_ms: int
    time_signature: int

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _to_cypher_structure():
        pass