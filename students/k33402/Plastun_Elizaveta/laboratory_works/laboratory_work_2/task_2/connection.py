import psycopg2

class DBConn:
    INSERT_SQL = """INSERT INTO public.books(title, price) VALUES (%s, %s)"""

    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="laboratory_work_2",
            user="postgres",
            password="shpornik",
            host="localhost",
            port="5432"
        )
        return conn