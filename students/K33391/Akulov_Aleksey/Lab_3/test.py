import psycopg2
from psycopg2 import sql

def check_connection(database_url):
    print(database_url)
    try:
        # Подключение к базе данных
        conn = psycopg2.connect(database_url)

        # Создание курсора для выполнения SQL-запросов
        cur = conn.cursor()

        # Выполнение запроса для получения версии базы данных
        cur.execute("SELECT version();")

        # Получение результата
        db_version = cur.fetchone()
        print(f"Connected to database. PostgreSQL version: {db_version[0]}")

        # Закрытие курсора и соединения
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Unable to connect to the database: {e}")

if __name__ == '__main__':
    # Ваша строка подключения
    database_url = "postgresql://postgres:@Local:5433/money_db"

    # Проверка подключения
    check_connection(database_url)