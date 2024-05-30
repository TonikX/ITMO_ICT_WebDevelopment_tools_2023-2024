from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    redis_host: str
    redis_port: int

    rabbitmq_host: str
    rabbitmq_port: int

    security_secret_key: str
    security_algorithm: str
    security_access_token_expire_minutes: int

    model_config = SettingsConfigDict()


settings = Settings()