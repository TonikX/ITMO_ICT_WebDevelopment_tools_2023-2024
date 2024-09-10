import psycopg2
from dotenv import load_dotenv
import os


# Класс базы данных
class DBConn:
    # SQL команда для вставки книг, %s будут заменять на переданные параметры
    # public - схема в бд, books - таблица внутри схемы
    INSERT_SQL = """INSERT INTO public.books(title, price) VALUES (%s, %s);"""

    # Аннотация/декоратор статического метода - метод, который не привязан к состоянию экземпляра или класса
    # (не нужна ссылка на сам класс 'self')
    @staticmethod
    def connect_to_database():
        load_dotenv()
        conn = psycopg2.connect(dbname=os.getenv("DB_NAME"), user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD"), host=os.getenv("DB_HOST"), port=os.getenv("DB_PORT"))  # подключаемся к этой бд и возвращаем эту связь
        conn.cursor().execute("CREATE TABLE IF NOT EXISTS public.books (id serial PRIMARY KEY, title text, price numeric);")
        conn.commit()
        return conn
