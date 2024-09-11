from pydantic_settings import SettingsConfigDict

from . import base


class Database(base.Base):
    port: int
    host: str = 'localhost'
    user: str
    password: str

    model_config = SettingsConfigDict(env_prefix="postgres_")

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/"
