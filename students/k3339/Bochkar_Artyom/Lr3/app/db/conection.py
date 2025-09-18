from sqlmodel import SQLModel, Session, create_engine
import os
from dotenv import load_dotenv

load_dotenv()

DB_ADMIN = os.getenv("DB_ADMIN")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_ADMIN, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise ValueError("Не все переменные окружения для БД найдены в .env файле")

DATABASE_URL = f"postgresql://{DB_ADMIN}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session