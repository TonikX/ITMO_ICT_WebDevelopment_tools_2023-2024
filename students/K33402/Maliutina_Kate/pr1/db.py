from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv('.env')  # загрузка переменных среды (энвы) из файла .env
db_url = os.getenv('DB_ADMIN')  # получение переменной с ключом DB_ADMIN
engine = create_engine(db_url, echo=True)  # создание "движка БД" - экземпляр со всем необходимым для работы с БД
# echo=True включает вывод всех осуществляемых SQL-запросов в командную строку


def init_db():
    SQLModel.metadata.create_all(engine)  # создание всех табличек из контекста (пометка table=True)


def get_session():
    with Session(engine) as session:  # создание сессии из движка
        yield session  # возврат генератора - функция вычисления значения на лету (выполнился и не хранится в памяти)
