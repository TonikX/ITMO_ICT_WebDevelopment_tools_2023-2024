import os

from dotenv import load_dotenv
from pydantic import BaseConfig

print("before l", os.getenv('DATABASE_URL'))
load_dotenv()
print("after l", os.getenv('DATABASE_URL'))
class Config(BaseConfig):
    # db_host = os.getenv("DB_HOST", "localhost")
    # db_port = os.getenv("DB_PORT", 5432)
    # db_user = os.getenv("DB_USER", "moni")
    # db_password = os.getenv("DB_PASSWORD", "123")
    # db_name = os.getenv("DB_NAME", "baza3")
    # db_uri = f'postgresql://{db_user}:{db_password}@{db_host}/{db_name}'
    db_uri = os.getenv('DATABASE_URL')
    hash_password_secret = os.getenv("HASH_PASSWORD_SECRET", "secret")
    #sqlalchemy.url = driver://user:pass@localhost/dbname

config = Config()
