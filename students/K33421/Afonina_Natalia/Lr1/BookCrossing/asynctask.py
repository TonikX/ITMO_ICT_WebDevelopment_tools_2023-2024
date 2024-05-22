import aiohttp
import asyncio
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from connection import engine
from models import Author
from time import time

Session = sessionmaker(bind=engine)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def parse_and_save_author(url, session):
    html = await fetch(url, session)
    soup = BeautifulSoup(html, 'html.parser')

    content_div = soup.find('div', id='mw-content-text')
    if not content_div:
        print(f"Content div not found for {url}")
        return

    for ul in content_div.find_all('ul', recursive=True):
        for li in ul.find_all('li', recursive=False):
            author_tag = li.find('a')
            if author_tag:
                author_name = author_tag.get_text()
                if author_name:
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
                else:
                    print(f"Author name not found in {url}")


async def main_async(urls):
    start_time = time()
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save_author(url, session) for url in urls]
        await asyncio.gather(*tasks)
    end_time = time()
    print(f"Async: {end_time - start_time} seconds")


urls = [
    "https://en.wikipedia.org/wiki/List_of_poets",
    "https://en.wikipedia.org/wiki/List_of_children%27s_literature_writers",
    "https://en.wikipedia.org/wiki/List_of_fantasy_authors"
]

asyncio.run(main_async(urls))
