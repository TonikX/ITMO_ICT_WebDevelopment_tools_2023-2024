import multiprocessing
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
        'https://www.google.com',
        'https://www.youtube.com',
        'https://www.vk.com',
        # Добавьте другие URL
    ]

    start_time = time.time()
    processes = []

    for url in urls:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Multiprocessing finished in {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    main()
