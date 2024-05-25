import psycopg2


class DBConn:
    INSERT_SQL = """INSERT INTO public.books(title, price) VALUES (%s, %s)"""

    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="web_books_db",
            user="ekaterinamalyutina",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return conn
