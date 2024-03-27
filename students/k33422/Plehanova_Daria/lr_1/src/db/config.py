from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    scheme: str
    user: str
    password: str
    host: str
    port: str
    name: str

    model_config = SettingsConfigDict(
        env_prefix='db_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def url(self) -> PostgresDsn:
        return f"{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


settings = Settings()
