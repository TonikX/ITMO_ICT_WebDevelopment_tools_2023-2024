# Задание 2. DataBaseConnection

В этом файле реализовано подключение к базе данных.

### Код

    import psycopg2
    
    
    class DataBaseConnection:
        INSERT_SQL = """INSERT INTO public.task(title, description, deadline, 
                                                created_date, priority, status, 
                                                category_id, user_id)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    
        @staticmethod
        def connect_to_database():
            conn = psycopg2.connect(
                dbname="tasks_db",
                user="postgres",
                password="12345",
                host="localhost",
                port="5433"
            )
            return conn
