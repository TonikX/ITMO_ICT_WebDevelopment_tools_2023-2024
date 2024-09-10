import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


class DBConn:
    # SQL команда для вставки книг, %s будут заменять на переданные параметры
    INSERT_SQL = """INSERT INTO public.articles(title, author, datetime) VALUES (%s, %s, %s)"""

    # таблица содержит все поля с типом text
    # Аннотация/декоратор статического метода - метод, который не привязан к состоянию экземпляра или класса
    # (не нужна ссылка на сам класс 'self')
    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        conn.cursor().execute(
            "CREATE TABLE IF NOT EXISTS public.articles ("
            "id serial PRIMARY KEY, "
            "title text, "
            "author text, "
            "datetime text"
            ");")
        conn.commit()
        return conn
