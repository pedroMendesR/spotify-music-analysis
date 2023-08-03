from os import getenv
from typing import Dict, List, TypeVar, Union

from dotenv import load_dotenv
from requests import get

from client.Config import ClientConfig

load_dotenv()

T = TypeVar("T")


class DataClient:
    config: ClientConfig
    api_url: str = "https://api.spotify.com/v1"
    api_auth_token: str = getenv("SPOTIFY_AUTH_TOKEN")
    api_request_headers: Dict[str, str] = {"Authorization": f"Bearer {api_auth_token}"}

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get(
        self, url: str, params: Dict[str, Union[str, int, float, List]] = None
    ) -> T:
        response = get(f"{self.api_url}{url}", params, headers=self.api_request_headers)
        return response.json()
