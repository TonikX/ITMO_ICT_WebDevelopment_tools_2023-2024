from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv
from alembic.config import Config

load_dotenv()
db_url = os.getenv('DB_ADMIN')
# db_url = 'postgresql://postgres:Kirill307477@localhost/pract3'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
