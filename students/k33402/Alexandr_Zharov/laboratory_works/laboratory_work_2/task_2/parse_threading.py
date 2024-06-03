import threading
import requests
from bs4 import BeautifulSoup
import psycopg2
from psycopg2 import sql
import time

DATABASE_URL = "postgresql://postgres:23465@localhost/laboratory_work_2"

def create_table_if_not_exists():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS pages_3 (
                id SERIAL PRIMARY KEY,
                url TEXT NOT NULL,
                title TEXT NOT NULL
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Table 'pages' created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")

def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO pages_3 (url, title) VALUES (%s, %s)",
            (url, title)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"Title of {url}: {title}")
    except psycopg2.Error as e:
        print(f"Error saving data for {url}: {e}")

def main():
    urls = ["https://github.com/", "https://gitlab.com/", "https://hd.kinopoisk.ru/"]

    create_table_if_not_exists()

    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Затраченное время: {execution_time}")
