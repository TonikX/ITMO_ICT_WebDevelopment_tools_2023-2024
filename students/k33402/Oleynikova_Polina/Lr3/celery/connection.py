import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

class DataBaseConnection:
    INSERT_SQL = """INSERT INTO public.author(name, bio) VALUES (%s, %s)"""

    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASS'),
            host=os.getenv('DB_HOST'),
            port="5432"
        )
        return conn