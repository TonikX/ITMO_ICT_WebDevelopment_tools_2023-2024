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
