import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/time_manager_db",
    )
    workers: int = int(os.getenv("WORKERS", "4"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
