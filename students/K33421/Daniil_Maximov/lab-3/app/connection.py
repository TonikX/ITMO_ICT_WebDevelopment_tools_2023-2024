import os

from dotenv import load_dotenv

from sqlmodel import SQLModel, Session, create_engine, text

load_dotenv()
db_url = os.getenv("DB_LINK")
engine = create_engine(db_url)


def init_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
