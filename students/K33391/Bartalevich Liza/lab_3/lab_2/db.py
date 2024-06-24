from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
import datetime
from sqlmodel import Field, SQLModel

load_dotenv()

db_url = os.getenv("DB_URL", 'postgresql://postgres:postgres@db:5432/web_data')

engine = create_engine(db_url, echo=True)


def create_database_session() -> Session:
    return Session(bind=engine)

def init_db() -> None:
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session



class Parce(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    article_title: str

init_db()