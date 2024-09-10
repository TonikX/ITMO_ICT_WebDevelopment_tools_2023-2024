from dotenv import load_dotenv
import os

from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy_utils import database_exists, create_database

load_dotenv('.env')
db_url = os.getenv('DB_URL')
engine = create_engine(db_url, echo=True)  # echo=True вывод SQL-запросов в терминал
if not database_exists(engine.url):
    create_database(engine.url)


def init_db():
    SQLModel.metadata.create_all(engine)  # создание всех табличек из контекста (пометка table=True)


def get_session():
    with Session(engine) as session:  # создание сессии из движка
        yield session  # возврат генератора - функция вычисления значения на лету (выполнился и не хранится в памяти)
