from dotenv import load_dotenv
import os

from sqlmodel import SQLModel, Session, create_engine

load_dotenv('.env')
db_url = os.getenv('DB_URL')
engine = create_engine(db_url, echo=True)  # echo=True вывод SQL-запросов в терминал


def init_db():
    SQLModel.metadata.create_all(engine)  # создание всех табличек из контекста (пометка table=True)


def get_session():
    with Session(engine) as session:  # создание сессии из движка
        yield session  # возврат генератора - функция вычисления значения на лету (выполнился и не хранится в памяти)
