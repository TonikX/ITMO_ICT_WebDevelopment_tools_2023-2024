from .auntification import Auntification
from .database import Database

__all__ = [
    "database",
]

database = Database()  # type: ignore
auntification = Auntification()  # type: ignore
