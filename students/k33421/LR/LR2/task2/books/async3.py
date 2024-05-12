import aiohttp
import asyncio
from bs4 import BeautifulSoup
import time
import asyncpg


def create_aiohttp_session():
    return aiohttp.ClientSession()


async def parse_and_save(url, session):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        book_entries = soup.find_all("article", class_="product_pod")

        conn = await asyncpg.connect('postgresql://postgres:qwerty12345@localhost:5432/books_info')
        try:
            for entry in book_entries:
                title_tag = entry.find("h3")
                book_title = title_tag.find("a")["title"]

                price_tag = entry.find("p", class_="price_color")
                book_price = price_tag.text.strip("Â")
                if entry == book_entries[0]:
                    print(f"Book Title: {book_title}")
                    print(f"Book Price: {book_price}")
                    print()

                await conn.execute('''
                            INSERT INTO books (title, price) VALUES($1, $2)
                        ''', book_title, book_price)

        finally:
            await conn.close()


async def main(pages):
    tasks = []
    async with create_aiohttp_session() as session:
        for page in pages:
            task = asyncio.create_task(parse_and_save(f'https://books.toscrape.com/catalogue/category/books_1/page-{page}.html', session))
            tasks.append(task)
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    pages = [1, 2, 3, 4]
    start_time = time.time()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main(pages))
    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Async time: {execution_time}")
