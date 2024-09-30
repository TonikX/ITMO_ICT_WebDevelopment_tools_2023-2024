from sqlmodel import SQLModel, Session, create_engine, Field
import os
from dotenv import load_dotenv

load_dotenv()
db_url = 'postgresql://postgres:123@db:5432/lab3'
engine = create_engine(db_url, echo=True)

class Site(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str
    title: str
    method: str

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    session = Session()
    try:
        yield session
    finally:
        session.close()