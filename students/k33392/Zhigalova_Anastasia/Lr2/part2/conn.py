
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from lr2.part2.db import Task


DB_URL = 'postgresql://postgres:12345@localhost/mero'


engine = create_engine(DB_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

   
