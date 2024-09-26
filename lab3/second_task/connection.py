from sqlmodel import SQLModel, Session, create_engine, Field
from contextlib import contextmanager
from dotenv import load_dotenv
import os

load_dotenv()
db_url = os.getenv('DATABASE_URL', 'postgresql://postgres:1216@db:5432/db_lab3')
engine = create_engine(db_url, echo=True)

class Site(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str
    title: str
    method: str

def init_db():
    SQLModel.metadata.create_all(engine)


@contextmanager
def get_session():
    with Session(engine) as session:
        yield session
