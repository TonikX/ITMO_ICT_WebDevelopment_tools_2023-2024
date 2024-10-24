from sqlmodel import Session, create_engine
from models import *
import dotenv
import os


dotenv.load_dotenv()

engine_url = os.getenv("DB_URL")
print(engine_url)

engine = create_engine(engine_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
