import os

from pydantic import BaseConfig


class Config(BaseConfig):
    db_host = os.getenv("DB_HOST", "db")
    db_port = os.getenv("DB_PORT", 5432)
    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_name = os.getenv("DB_NAME", "hfm")
    db_uri = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
    hash_password_secret = os.getenv("HASH_PASSWORD_SECRET", "secret")


config = Config()
