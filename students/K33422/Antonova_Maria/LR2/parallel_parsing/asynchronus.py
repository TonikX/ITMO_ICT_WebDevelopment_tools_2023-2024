import asyncio
import aiohttp
import psycopg2
from bs4 import BeautifulSoup


def create_aiohttp_session():
    return aiohttp.ClientSession()


async def parse_and_save(url, session):
    async with session.get(url) as response:
        html = await response.text()
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string

        # Соединение с базой данных
        conn = psycopg2.connect("dbname=baza3 user=moni password=123 host=localhost")
        cur = conn.cursor()

        # Сохранение заголовка в базу данных
        cur.execute("INSERT INTO pages_2 (url, title) VALUES (%s, %s)", (url, title))
        conn.commit()

        print(f"Title of {url}: {title}")

        cur.close()
        conn.close()


async def main():
    urls = ["https://platffin.com", "https://lamoda.ru", "https://olsi-trade.ru"]
    tasks = []

    async with create_aiohttp_session() as session:
        for url in urls:
            task = asyncio.create_task(parse_and_save(url, session))
            tasks.append(task)

        await asyncio.gather(*tasks)


if __name__ == "__main__":
    import time

    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")