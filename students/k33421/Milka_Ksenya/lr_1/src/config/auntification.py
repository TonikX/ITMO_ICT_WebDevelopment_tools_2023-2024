from pydantic_settings import SettingsConfigDict

from . import base


class Auntification(base.Base):
    algorithm: str
    expires_in: int
    private_key_path: str
    public_key_path: str

    model_config = SettingsConfigDict(env_prefix="auntification_")

    @property
    def private_key(self) -> str:
        with open(self.private_key_path) as f:
            return f.read()

    @property
    def public_key(self) -> str:
        with open(self.public_key_path) as f:
            return f.read()
