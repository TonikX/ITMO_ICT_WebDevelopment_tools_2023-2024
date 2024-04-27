from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    user: str
    password: str
    scheme: str
    host: str
    port: int
    name: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='db_',
    )

    def get_dsn(self) -> PostgresDsn:
        return f'{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}'


settings = Settings()
