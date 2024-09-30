import threading
import requests
from bs4 import BeautifulSoup
import time
from database import get_session, Site, init_db

init_db()  # Initialize the database

def parse_and_save(url):
    session = get_session()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find('title').text
    site = Site(url=url, title=title, method='GET')
    session.add(site)
    session.commit()
    session.close()
    print(f"{url} - {title}")

def threading_example():
    urls = [
        'https://www.example.com',
        'https://www.google.com',
        'https://www.python.org',
        'https://www.stackoverflow.com',
        'https://www.github.com'
    ]
    threads = []

    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    start_time = time.time()
    threading_example()
    end_time = time.time()
    print(f"Threading time: {end_time - start_time:.4f} seconds")