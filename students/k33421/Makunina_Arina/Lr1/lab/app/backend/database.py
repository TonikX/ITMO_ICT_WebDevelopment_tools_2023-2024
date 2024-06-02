from sqlmodel import create_engine, Session
import os
from dotenv import load_dotenv


load_dotenv()  # Загружает переменные окружения из файла .env

DATABASE_URL = os.getenv("DB_ADMIN")  # Получает URL базы данных
engine = create_engine(DATABASE_URL)  # Создает движок SQLAlchemy для подключения к бд


def get_session():
    with Session(engine) as session:
        yield session  # Создает и управляет сессией базы данных
