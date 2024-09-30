import multiprocessing
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

def multiprocessing_example():
    urls = [
        'https://www.example.com',
        'https://www.google.com',
        'https://www.python.org',
        'https://www.stackoverflow.com',
        'https://www.github.com'
    ]

    with multiprocessing.Pool() as pool:
        pool.map(parse_and_save, urls)

if __name__ == "__main__":
    start_time = time.time()
    multiprocessing_example()
    end_time = time.time()
    print(f"Multiprocessing time: {end_time - start_time:.4f} seconds")