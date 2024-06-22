import threading
import requests
from bs4 import BeautifulSoup
from sqlmodel import Session
from database import WebPage, create_db_and_tables, engine
import sys

def parse_and_save(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title'

        with Session(engine) as session:
            webpage = WebPage(url=url, title=title)
            session.add(webpage)
            session.commit()
    except Exception as e:
        print(f"Ошибка парсинга {url}: {e}")

def worker(urls):
    for url in urls:
        parse_and_save(url)

def main(urls):
    num_threads = 4
    create_db_and_tables()
    threads = []
    for i in range(num_threads):
        part = urls[i::num_threads]
        thread = threading.Thread(target=worker, args=(part,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    import time
    urls = sys.argv[1:]
    if not urls:
        print("Не предоставлены url для парсинга")
        sys.exit(1)
    start_time = time.time()
    main(urls)
    end_time = time.time()
    print(f"Threading занял: {end_time - start_time} секунд")
