import threading
import requests
from bs4 import BeautifulSoup
import psycopg2
import time

DB_URL = 'postgresql://postgres:12345@localhost/finances'


def save_to_db(url, title):
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO page (url, title) VALUES (%s, %s)", (url, title))
    conn.commit()
    cursor.close()
    conn.close()


def parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'
    save_to_db(url, title)
    print(f"Processed: {url} with title: {title}")


def main():
    urls = [
        'https://example.com',
        'https://www.python.org',
        'https://www.wikipedia.org'
        # Добавьте другие URL
    ]

    start_time = time.time()
    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Threading finished in {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    main()
