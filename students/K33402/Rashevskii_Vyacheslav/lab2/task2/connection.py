import psycopg2


class DB:
    INSERT_SQL = """insert into public.prs(title, date, author) values (%s, %s, %s);"""

    @staticmethod
    def connect():
        con = psycopg2.connect(
            dbname="web_tools_db",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        return con
