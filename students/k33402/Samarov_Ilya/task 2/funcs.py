import asyncio
import aiohttp
import multiprocessing
import threading
from bs4 import BeautifulSoup
import requests
import time
from db import create_database_session, Site, init_db


urls = [
    'https://www.bookvoed.ru/catalog/knigi-s-avtografom-4435',
    'https://www.bookvoed.ru/catalog/detskie-knigi-1159',
    'https://www.bookvoed.ru/catalog/samoobrazovanie-i-razvitie-4560',
    'https://www.bookvoed.ru/catalog/khobbi-i-dosug-4056',
    'https://www.bookvoed.ru/catalog/estestvennye-nauki-1347',
    'https://www.bookvoed.ru/catalog/religiya-1437',
]


async def async_parse_and_save(session: aiohttp.ClientSession, url: str):
    async with session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, "html.parser")
        title = parsed_html.title.string

        db_session = create_database_session()
        new_article = Site(
            url=url, title=title, method='async'
        )

        db_session.add(new_article)
        db_session.commit()
        db_session.refresh(new_article)


async def async_main():
    async with aiohttp.ClientSession() as session:
        tasks = [async_parse_and_save(session, url) for url in urls]
        await asyncio.gather(*tasks)


def mlp_parse_and_save(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else 'No title'

    db_session = create_database_session()
    new_article = Site(
        url=url, title=title, method='multiproc'
    )
    db_session.add(new_article)
    db_session.commit()
    db_session.refresh(new_article)


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

    db_session = create_database_session()
    new_article = Site(
        url=url, title=title, method='thread'
    )
    db_session.add(new_article)
    db_session.commit()
    db_session.refresh(new_article)


def thread_main():
    threads = []
    for url in urls:
        thread = threading.Thread(target=thread_parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":

    init_db()

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