import psycopg2

# Класс базы данных
class DBConn:
    # SQL команда для вставки книг, %s будут заменять на переданные параметры
    # public - схема в бд, books - таблица внутри схемы
    INSERT_SQL = """INSERT INTO public.books(title, price) VALUES (%s, %s)"""

    # Аннотация/декоратор статического метода - метод, который не привязан к состоянию экземпляра или класса
    # (не нужна ссылка на сам класс 'self')
    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="web_books_db",  # название бд
            user="ekaterinamalyutina",  # имя пользователя
            password="postgres",  # пароль пользователя
            host="localhost",  # хост
            port="5432"  # дефолтный порт
        )  # подключаемся к этой бд и возвращаем эту связь
        return conn
