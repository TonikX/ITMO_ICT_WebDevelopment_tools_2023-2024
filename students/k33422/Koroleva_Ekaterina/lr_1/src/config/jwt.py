from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    private_key: str
    public_key: str
    algorithm: str
    expire_minutes: int

    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env',
        env_prefix='jwt_',
    )


settings = Settings()
