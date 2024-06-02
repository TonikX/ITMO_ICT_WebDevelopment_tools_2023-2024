from .celery import celery
from .parse_url import parse_url
from .api_client import add_cities

from typing import List

@celery.task
def parse_urls_task(url):
    result = parse_url(url)
    if result and "error" not in result:
        add_cities(result)
