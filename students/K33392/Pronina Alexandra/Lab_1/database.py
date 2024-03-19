import os

from sqlalchemy import create_engine
from databases import Database
from decouple import config
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

DATABASE_URL = "sqlite:///./tourism.db"  # Используйте ваш URL-адрес базы данных

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
