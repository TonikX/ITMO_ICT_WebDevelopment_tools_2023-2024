import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


class DB:
    INSERT_SQL = """insert into public.prs(title, date, author) values (%s, %s, %s);"""

    @staticmethod
    def connect():
        con = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        con.cursor().execute("CREATE TABLE IF NOT EXISTS public.prs (id serial PRIMARY KEY, title text, date text, author text);")
        con.commit()
        return con
