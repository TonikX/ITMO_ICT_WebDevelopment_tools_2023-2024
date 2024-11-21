import psycopg2


class DataBaseConnection:
    INSERT_SQL = """INSERT INTO public.task(title, description, deadline, 
                                            created_date, priority, status, 
                                            category_id, user_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    @staticmethod
    def connect_to_database():
        conn = psycopg2.connect(
            dbname="timetable",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        return conn