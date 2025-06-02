import os
import requests

from app import celery_app

from .celery_app import celery_app

from urls import urls


@celery_app.task(name="app.tasks.parse_url_task")
def parse_url_task(url: str):
    parser_url = os.getenv("PARSER_URL", "http://parser_app:8001/parse")
    response = requests.post(parser_url, json={"url": url})
    response.raise_for_status()
    return response.json()

@celery_app.task(name="app.tasks.run_periodic_parsing")
def run_periodic_parsing():
    for url in urls:
        parse_url_task.delay(url)
    return f"Dispatched {len(urls)} parsing tasks"
