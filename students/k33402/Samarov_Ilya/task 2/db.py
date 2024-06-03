from sqlmodel import SQLModel, create_engine, Session, Field
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv("DB_URL")
engine = create_engine(db_url, echo=False)


def create_database_session() -> Session:
    return Session(bind=engine)


class Site(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str
    title: str
    method: str


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


