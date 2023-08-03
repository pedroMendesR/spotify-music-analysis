from dataclasses import dataclass
from os import getenv
from typing import TypeVar, Union

from dotenv import load_dotenv
from neo4j import Driver, GraphDatabase
from neo4j.exceptions import DatabaseError, DriverError

load_dotenv()

DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PROTOCOL = getenv("DB_PROTOCOL")
DB_PORT = getenv("DB_PORT")

CONNECTION_URI = f"{DB_PROTOCOL}://{DB_HOST}:{DB_PORT}"

T = TypeVar("T")


@dataclass
class DatabaseDriver:
    driver: Driver
    database: str = "neo4j"

    def __init__(self, database_name: str) -> None:
        self.driver = GraphDatabase.driver(
            uri=CONNECTION_URI, auth=(DB_USER, DB_PASSWORD)
        )
        self.database = database_name

    def close(self) -> None:
        self.driver.close()

    def exec(self, query: str) -> Union[T, None]:
        try:
            with self.driver.session() as session:
                records = session.run(query)
                return records
        except (DriverError, DatabaseError) as exception:
            print(f"Erro: {exception}")
        finally:
            self.close()
