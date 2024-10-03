from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os
import urllib.parse

load_dotenv()
db_dialect = os.getenv("DB_DIALECT")
db_driver = ""
db_user = os.getenv("DB_USER")
db_password = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

db_url = f"{db_dialect}{db_driver}://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
