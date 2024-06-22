from sqlmodel import SQLModel, Field, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/database")

engine = create_engine(DATABASE_URL)

class WebPage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    title: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)