from sqlmodel import SQLModel, Session, create_engine
from models import *
import os
from dotenv import load_dotenv


load_dotenv()
DB_URL = os.getenv('DB_URL')

# нужно прописать на уровне БД 'CREATE EXTENSION IF NOT EXISTS vector', я через psql shell делала
engine = create_engine(DB_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
