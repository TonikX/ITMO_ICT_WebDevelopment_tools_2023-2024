from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv
db_url = 'postgresql://postgres:Scalapendra1219212712192127@localhost:5433/book_database'
#load_dotenv()
#db_url = os.getenv('DB_URL')

from config import *
#from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
#db_session = sessionmaker(bind=engine)
#db_session = Session()

#engine = create_engine(db_url, echo=True)
db_session = Session(bind=engine)
def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session