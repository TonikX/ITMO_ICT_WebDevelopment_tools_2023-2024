import multiprocessing
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

    for ul in content_div.find_all('ul', recursive=True):
        for li in ul.find_all('li', recursive=False):
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


def chunk_list(lst, n):
    """Разделяет список на n равных частей."""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]


def main_multiprocessing(urls):
    start_time = time()
    with multiprocessing.Pool() as pool:
        pool.map(parse_and_save_author, urls)
    end_time = time()
    print(f"Multiprocessing: {end_time - start_time} seconds")


urls = [
    "https://en.wikipedia.org/wiki/List_of_poets",
    "https://en.wikipedia.org/wiki/List_of_children%27s_literature_writers",
    "https://en.wikipedia.org/wiki/List_of_fantasy_authors"
]

num_processes = 3  # Количество процессов
chunks = chunk_list(urls, num_processes)

if __name__ == '__main__':
    processes = []
    for chunk in chunks:
        p = multiprocessing.Process(target=main_multiprocessing, args=(chunk,))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
