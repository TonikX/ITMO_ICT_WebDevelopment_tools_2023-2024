from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    private_key: str
    public_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(
        env_prefix='auth_',
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )


settings = Settings()
