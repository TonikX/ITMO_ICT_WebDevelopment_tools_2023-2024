from .auntification import Auntification
from .database import Database
from .redis import Redis

__all__ = [
    "database",
]

database = Database()  # type: ignore
auntification = Auntification()  # type: ignore
redis = Redis()  # type: ignore
