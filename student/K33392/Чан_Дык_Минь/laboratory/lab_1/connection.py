from sqlmodel import SQLModel, Session, create_engine
import os
from decouple import config


BASE_DIR=os.path.dirname(os.path.realpath(__file__))
conn_str=config("DB_URL")
engine=create_engine(conn_str, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session