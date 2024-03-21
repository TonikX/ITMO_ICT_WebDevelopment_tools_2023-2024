from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    port: int
    user: str
    password: str
    name: str


class Settings(BaseSettings):
    database: DatabaseSettings

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent.parent / ".env", env_nested_delimiter="__"
    )


settings = Settings()
