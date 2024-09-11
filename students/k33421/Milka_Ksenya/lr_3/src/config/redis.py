from pydantic_settings import SettingsConfigDict

from . import base


class Redis(base.Base):
    port: int
    host: str = 'localhost'

    model_config = SettingsConfigDict(env_prefix="REDIS_")

    @property
    def dsn(self) -> str:
        return f"redis://{self.host}:{self.port}/0"
