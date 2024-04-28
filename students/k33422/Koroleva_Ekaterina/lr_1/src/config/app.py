from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    title: str
    debug: bool

    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env',
        env_prefix='app_',
    )


settings = Settings()
