from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    max_limit: int

    model_config = SettingsConfigDict(
        extra='ignore',
        env_file='.env',
        env_prefix='pag_',
    )


settings = Settings()
