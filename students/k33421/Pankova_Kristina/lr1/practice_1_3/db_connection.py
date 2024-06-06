from sqlmodel import SQLModel, Session, create_engine
from models import *

db_url = 'postgresql://postgres:1234@localhost:5432/warriors_db'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


