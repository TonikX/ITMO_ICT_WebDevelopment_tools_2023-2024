from urllib.request import urlopen

from bs4 import BeautifulSoup
from pydantic import BaseModel

from .app import app
import logging


class WebPage(BaseModel):
    title: str


def parse_page(url: str) -> WebPage:
    logger = logging.getLogger()
    logger.info('Requesting url %s', url)
    soup = BeautifulSoup(urlopen(url), features="html.parser")
    title = soup.title.get_text()
    logger.info('Got response with title \'%s\'', title)
    page = WebPage(title=title)
    return page


@app.task
def long_running_task(url):
    return parse_page(url)
