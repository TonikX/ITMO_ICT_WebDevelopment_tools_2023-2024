import os

from pydantic import BaseConfig


class Config(BaseConfig):
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", 5432)
    db_user = os.getenv("DB_USER", "moni")
    db_password = os.getenv("DB_PASSWORD", "123")
    db_name = os.getenv("DB_NAME", "baza3")
    db_uri = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'


config = Config()
