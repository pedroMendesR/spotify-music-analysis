from datetime import datetime
from os import getenv
from typing import Dict, List, TypeVar, Union

from dotenv import load_dotenv
from requests import get

from .Config import ClientConfig

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

    def update_auth_token(self, new_token: str):
        self.api_auth_token = new_token
        self.api_request_headers["Authorization"] = f"Bearer {new_token}"

    def get(
        self, url: str, params: Dict[str, Union[str, int, float, List]] = None
    ) -> T:
        while True:
            response = None
            try:
                response = get(
                    f"{self.api_url}{url}", params, headers=self.api_request_headers
                )
                if response.status_code == 200:
                    return response.json(), response.status_code
                elif response.status_code == 401:
                    self.update_auth_token(
                        input(
                            "(if) O token de autenticação expirou, favor inserir outro:\n"
                        )
                    )
                elif response.status_code == 429:
                    print(
                        f"\033[91m {datetime.now()} (if) TOO MANY REQUESTS!! Status: [{response.status_code}]: {response.reason} \033[0m"
                    )
                    input("Continuar...")
            except:
                print()
                print(
                    f"\033[91m REQUISIÇÃO FALHOU!! Status: [{response.status_code}]: {response.reason} \033[0m"
                )
                exit(1)
            input(f"{datetime.now()} {response}")
