import psycopg2

class DBConn:
    # SQL команда для вставки книг, %s будут заменять на переданные параметры
    INSERT_SQL = """INSERT INTO public.articles(title, author, datetime) VALUES (%s, %s, %s)"""
    # таблица содержит все поля с типом text
    # Аннотация/декоратор статического метода - метод, который не привязан к состоянию экземпляра или класса
    # (не нужна ссылка на сам класс 'self')
    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="web_articles_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return conn
