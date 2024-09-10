import asyncio
import aiohttp
import asyncpg
import multiprocessing
import threading
import psycopg2
from bs4 import BeautifulSoup
import requests
import time
from dotenv import load_dotenv
import os
load_dotenv()
db_url = os.getenv("DB_URL")
from db import init_db


urls = [
    "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html",
    "http://books.toscrape.com/catalogue/category/books/historical-fiction_4/index.html",
    "http://books.toscrape.com/catalogue/category/books/religion_12/index.html",
    "http://books.toscrape.com/catalogue/category/books/paranormal_24/index.html",
    "http://books.toscrape.com/catalogue/category/books/christian-fiction_34/index.html"
]


async def async_parse_and_save(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, "html.parser")
        title = parsed_html.title.string

        conn = await asyncpg.connect(os.getenv("DB_URL"))
        try:
            await conn.execute(
                "INSERT INTO site (url, title, process_type) VALUES ($1, $2, $3)",
                url, title, 'async'
            )
        finally:
            await conn.close()



async def async_main():
    async with aiohttp.ClientSession() as session:
        tasks = [async_parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)


def mlp_parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No title'

    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()

    curs.execute(
        "INSERT INTO site (url, title, process_type) VALUES (%s, %s, %s)",
        (url, title, 'multyprocess')
    )

    conn.commit()
    curs.close()
    conn.close()



def mlp_main():
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=mlp_parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


def thread_parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No title'

    conn = psycopg2.connect(os.getenv("DB_URL"))
    curs = conn.cursor()

    curs.execute(
        "INSERT INTO site (url, title, process_type) VALUES (%s, %s, %s)",
        (url, title, 'threading')
    )
    conn.commit()

    curs.close()
    conn.close()


def thread_main():
    threads = []
    for url in urls:
        thread = threading.Thread(target=thread_parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":

    asyncio.run(init_db())

    start_time = time.time()
    asyncio.run(async_main())
    end_time = time.time()
    print(f"async {end_time - start_time}\n")

    start_time = time.time()
    mlp_main()
    end_time = time.time()
    print(f"muliprocess {end_time - start_time}\n")

    start_time = time.time()
    thread_main()
    end_time = time.time()
    print(f"thread {end_time - start_time}\n")