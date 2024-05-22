# Задача 2
Напишите программу на Python для параллельного парсинга нескольких веб-страниц с сохранением данных в базу данных с использованием подходов threading, multiprocessing и async. Каждая программа должна парсить информацию с нескольких веб-сайтов, сохранять их в базу данных.

## Threading
```python
import threading
import logging
import requests
from urllib.request import urlopen
from db import save_web_page, WebPage
from bs4 import BeautifulSoup
from shared import URLS
from util import get_function_execution_time_sec, bootstrap_environment


def parse_and_save(url: str) -> None:
    logger = logging.getLogger(f'Thread {threading.current_thread().ident}')
    logger.info('Requesting url %s', url)
    soup = BeautifulSoup(urlopen(url), features="html.parser")
    title = soup.title.get_text()
    logger.info('Got response with title \'%s\'', title)
    page = WebPage(title=title)
    try:
        page = save_web_page(page)
        logger.info('Web page saved. Generated id is %s', page.id)
    except Exception as e:
        logger.error('Failed to save web page')
        logger.exception(e)


def main():
    threads = []
    for url in URLS:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    bootstrap_environment()
    logger = logging.getLogger('main')
    time_sec, *_ = get_function_execution_time_sec(main)
    logger.info(f"Затраченное время - {time_sec:.3f} сек")
```

## Multiprocessing
```python
import multiprocessing
import logging
from urllib.request import urlopen
from db import save_web_page, WebPage
from bs4 import BeautifulSoup
from shared import URLS
from util import get_function_execution_time_sec, bootstrap_environment


def __setup_logger():
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(processName)s %(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler('process.log')
    handler.setFormatter(formatter)
    if not len(logger.handlers):
        logger.addHandler(handler)

    return logger

def parse_and_save(url: str) -> None:
    logger = __setup_logger()

    logger.info('Requesting url %s', url)
    soup = BeautifulSoup(urlopen(url), features="html.parser")
    title = soup.title.get_text()
    logger.info('Got response with title \'%s\'', title)
    page = WebPage(title=title)
    try:
        page = save_web_page(page)
        logger.info('Web page saved. Generated id is %s', page.id)
    except Exception as e:
        logger.error('Failed to save web page')
        logger.exception(e)


def main():
    processes = []
    for url in URLS:
        process = multiprocessing.Process(target=parse_and_save, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    bootstrap_environment('process.log')
    logger = logging.getLogger('main')
    time_sec, *_ = get_function_execution_time_sec(main)
    logger.info(f"Затраченное время - {time_sec:.3f} сек")

```

## Async \ Await
```python
import asyncio
import logging
import aiohttp

from bs4 import BeautifulSoup

from db import WebPage, save_web_page
from util import bootstrap_environment, get_function_execution_time_sec_async
from shared import URLS


async def parse_and_save(client_session: aiohttp.ClientSession, url: str):
    logger = logging.getLogger()
    async with client_session.get(url) as response:
        html = await response.text()
        parsed_html = BeautifulSoup(html, 'html.parser')
        title = parsed_html.title.get_text()
        page = WebPage(title=title)
        try:
            page = save_web_page(page)
            logger.info('Web page saved. Generated id is %s', page.id)
        except Exception as e:
            logger.error('Failed to save web page')
            logger.exception(e)


async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [parse_and_save(session, url) for url in URLS]
        await asyncio.gather(*tasks)


async def wrapper():
    logger = logging.getLogger("Main")
    time_sec, *_ = await get_function_execution_time_sec_async(main)
    logger.info(f"Затраченное время - {time_sec:.3f} сек")


if __name__ == "__main__":
    bootstrap_environment()
    asyncio.run(wrapper())
```

## Выводы

| Method\Time | Threading | Multiprocessing | Async/Await |
|-------------|-----------|-----------------|-------------|
| 1           | 0.788     | 2.416           | 0.710       |
| 2           | 0.749     | 2.216           | 0.723       |
| 3           | 1.142     | 2.058           | 0.724       |
| Avg         | 0.846     | 2.230           | 0.719       |

Подход Async \ Await оказался самым быстрым в этой задаче из-за того, что он предназначен для исполнения I/O-bound задач (коей и является http-запрос страницы)
Подход threading оказался несколько хуже, поскольку при его использовании появляются накладные расходы на создание потоков и управлением ими.
Multiprocessing же снова оказался на последнем месте, поскольку он не предназначен для данного типа задач. При его использовании появляются ощутимые расходы на создание процессов и управление ими