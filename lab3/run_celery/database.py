from sqlmodel import SQLModel, create_engine, Session
import os
from schemas import Parse
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DB_URL")

engine = create_engine(db_url, echo=True)


def create_database_session() -> Session:
    return Session(bind=engine)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


init_db()
