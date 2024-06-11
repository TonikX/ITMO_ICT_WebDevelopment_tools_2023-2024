from sqlmodel import SQLModel, Session, create_engine
import os
from user_repo.user_models import User
from models import *
from dotenv import load_dotenv
# loading variables from .env file
load_dotenv()


db_url = os.getenv('DB_ADDRESS')
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
