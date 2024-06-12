import time
from typing import List
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp
import multiprocessing
import threading
from database import get_session, Site, init_db


def parse_and_save(url: str) -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.title.string if soup.title else "Без заголовка"

        db_session = get_session()
        new_article = Site(
            url=url, title=title, method='async'
        )

        db_session.add(new_article)
        db_session.commit()
        db_session.refresh(new_article)

        print(f"Успешно обработано: {url} - {title}")

    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")





def run_threading(urls) -> None:
    """Запускает парсинг с использованием threading."""
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


# --- Вариант 2: multiprocessing ---


def run_multiprocessing(urls) -> None:
    """Запускает парсинг с использованием multiprocessing."""
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(parse_and_save, urls)


# --- Вариант 3: async ---
async def fetch_page(session: aiohttp.ClientSession, url: str) -> str:
    """Асинхронно загружает страницу."""
    async with session.get(url, ssl=False) as response:
        return await response.text()


async def parse_and_save_async(session: aiohttp.ClientSession, url: str) -> None:
    """Асинхронно парсит и сохраняет данные."""
    try:
        html = await fetch_page(session, url)
        soup = BeautifulSoup(html, 'html.parser')
        title = soup.title.string if soup.title else "Без заголовка"

        db_session = get_session()
        new_article = Site(
            url=url, title=title, method='async'
        )

        db_session.add(new_article)
        db_session.commit()
        db_session.refresh(new_article)

        print(f"Успешно обработано: {url} - {title}")

    except Exception as e:
        print(f"Ошибка при обработке {url}: {e}")


async def run_async(urls: List[str]) -> None:
    """Запускает асинхронный парсинг."""
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save_async(session, url) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == "__main__":

    init_db()

    urls_to_parse = [
        # ... Ваши URL-адреса для парсинга
        'https://career.habr.com/vacancies?s%5B%5D=2&s%5B%5D=3&s%5B%5D=82&s%5B%5D=4&s%5B%5D=5&s%5B%5D=72&s%5B%5D=1&s%5B%5D=75&s%5B%5D=6&s%5B%5D=77&s%5B%5D=7&s%5B%5D=83&s%5B%5D=84&s%5B%5D=8&s%5B%5D=85&s%5B%5D=73&s%5B%5D=9&s%5B%5D=86&s%5B%5D=106&type=all',
        'https://career.habr.com/vacancies?s[]=2&s[]=3&s[]=82&s[]=4&s[]=5&s[]=72&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=84&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&s[]=106&sort=salary_desc&type=all',
        'https://career.habr.com/vacancies?s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true',
        'https://career.habr.com/vacancies?locations[]=c_699&s[]=1&s[]=75&s[]=6&s[]=77&s[]=7&s[]=83&s[]=8&s[]=85&s[]=73&s[]=9&s[]=86&sort=date&type=all&with_salary=true'
    ]

    # Разделение списка URL на равные части для каждого метода
    num_threads = 4
    num_processes = 4
    chunk_size = len(urls_to_parse) // num_threads  # Предполагаем одинаковое деление

    # Замеры времени для каждого метода
    start_time = time.time()
    run_threading(urls_to_parse)
    print(f"Время выполнения с threading: {time.time() - start_time:.5f} секунд")

    start_time = time.time()
    run_multiprocessing(urls_to_parse)
    print(f"Время выполнения с multiprocessing: {time.time() - start_time:.5f} секунд")

    start_time = time.time()
    asyncio.run(run_async(urls_to_parse))
    print(f"Время выполнения с async: {time.time() - start_time:.5f} секунд")
