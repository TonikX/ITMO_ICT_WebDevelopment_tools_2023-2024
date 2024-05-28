from sqlmodel import SQLModel, Session, create_engine
import os
from decouple import config


BASE_DIR=os.path.dirname(os.path.realpath(__file__))

DB_USER = config("DB_USER")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD")
DB_NAME = config("DB_NAME")
DB_HOST = config("DB_HOST")

DB_URL = f"postgresql://{DB_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine=create_engine(DB_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session