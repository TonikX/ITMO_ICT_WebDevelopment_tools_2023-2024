from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    security_secret_key: str
    security_algorithm: str
    security_access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=Path(__file__).resolve().parent.parent / ".env")


settings = Settings()