import threading
import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from connection import engine
from models import Author
from time import time

Session = sessionmaker(bind=engine)


def parse_and_save_author(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    content_div = soup.find('div', id='mw-content-text')

    if not content_div:
        print(f"Content div not found for {url}")
        return

    for ul in content_div.find_all('ul', recursive=True):  # Найти все ul внутри content_div
        for li in ul.find_all('li', recursive=False):  # Найти все li внутри каждого ul
            author_tag = li.find('a')
            if author_tag:
                author_name = author_tag.get_text()
                bio = li.get_text().split(author_name, 1)[-1].strip()

                with Session() as session:
                    author = session.query(Author).filter(Author.name == author_name).first()
                    if not author:
                        author = Author(name=author_name, bio=bio)
                        session.add(author)
                        session.commit()
                        print(f"Saved {author_name} from {url}")
                    else:
                        print(f"{author_name} already exists in the database")


def main_threading(urls):
    threads = []
    start_time = time()
    for url in urls:
        thread = threading.Thread(target=parse_and_save_author, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time()
    print(f"Threading: {end_time - start_time} seconds")


urls = [
    "https://en.wikipedia.org/wiki/List_of_poets",
    "https://en.wikipedia.org/wiki/List_of_children%27s_literature_writers",
    "https://en.wikipedia.org/wiki/List_of_fantasy_authors"
]

main_threading(urls)
