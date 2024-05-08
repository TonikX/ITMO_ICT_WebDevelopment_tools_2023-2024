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
