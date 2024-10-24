from sqlmodel import Session, create_engine
from models import *
import dotenv
import os

dotenv.load_dotenv()

# engine_url = os.getenv("ENGINE_URL")

engine = create_engine("postgresql://postgres:12345@localhost:5433/fastapi", echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
