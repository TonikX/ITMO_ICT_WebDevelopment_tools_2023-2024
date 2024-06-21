from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy_utils import database_exists, create_database
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv('DB_ADMIN')
engine = create_engine(db_url, echo=True)


def init_db():
    if not database_exists(engine.url):
        create_database(engine.url)
    # SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
 
def get_session():
    with Session(engine) as session:
        yield session
