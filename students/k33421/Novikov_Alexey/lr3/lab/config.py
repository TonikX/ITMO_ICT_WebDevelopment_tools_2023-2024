from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    host: str
    user: str
    password: str
    name: str


class RabbitMQSettings(BaseModel):
    host: str


class RedisSettings(BaseModel):
    host: str


class SecuritySettings(BaseModel):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Settings(BaseSettings):
    database: DatabaseSettings
    security: SecuritySettings
    redis: RedisSettings
    rabbitmq: RabbitMQSettings

    model_config = SettingsConfigDict(env_nested_delimiter="__")


settings = Settings()
