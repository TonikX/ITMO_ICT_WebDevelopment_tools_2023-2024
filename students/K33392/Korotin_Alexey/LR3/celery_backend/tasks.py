import logging
import os
from typing import TypedDict
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

from .app import app
from celery import Task
from dotenv import load_dotenv

load_dotenv()

CALLBACK_URL = os.getenv("CALLBACK_URL")

class WebPage(TypedDict):
    title: str


def parse_page(url: str) -> WebPage:
    logger = logging.getLogger()
    logger.info('Requesting url %s', url)
    soup = BeautifulSoup(urlopen(url), features="html.parser")
    title = soup.title.get_text()
    logger.info('Got response with title \'%s\'', title)
    page = WebPage(title=title)
    return page


class BaseTask(Task):

    def on_success(self, retval, task_id, args, kwargs):
        super().on_success(retval, task_id, args, kwargs)
        requests.post(CALLBACK_URL, params={'title': retval['title']})


@app.task(base=BaseTask)
def parse_task(url):
    return parse_page(url)
