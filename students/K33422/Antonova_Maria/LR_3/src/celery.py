import os

import requests
from celery import Celery
from src.adapters.db import SqlalchemyWorker
from src.repos.parser import parse_and_save

celery_app = Celery(__name__)
celery_app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://redis:6379")
celery_app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://redis:6379")


# @celery_app.task(name="parse_url_content")
# def parse_url_content(url: str):
#     parse_and_save(url)

import aiohttp

from src.adapters.db import SqlalchemyWorker
from src.celery import celery_app
from src.repos.parser import parse_and_save


@celery_app.task(name="parse_url_content") # задача celery - она выполняется синхронно
def parse_url_content(url: str): #метод
    #parse_and_save(url, html, sqlalchemy_worker)
    with requests.Session() as request_session:
        full_url = f'http://parser/parse?url={url}'
        response = request_session.post(full_url)
        response.raise_for_status()
        #html = await response.text()
        #parse_url_content.delay(url, html, sqlalchemy_worker) # вызов задачи
        return {"message": "Parsing is started"}