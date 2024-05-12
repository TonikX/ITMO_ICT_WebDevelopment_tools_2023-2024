import psycopg2


class DataBaseConnection:
    INSERT_SQL = """INSERT INTO public.author(name, bio) VALUES (%s, %s)"""

    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="web_db",
            user="",
            password="",
            host="localhost",
            port="5432"
        )
        return conn