import requests
import time
import random
from celery import Celery

import os
from dotenv import load_dotenv


load_dotenv()
parser_url = os.getenv('PARSER_URL')
redis_url = os.getenv('REDIS_URL')


celery_app = Celery('tasks', broker=redis_url, backend=redis_url)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    key = random.choice(["planes", "cruises", "trains", "airbnb", "hotels", "hostels"])
    sender.add_periodic_task(20.0, parse_celery.s(key))


@celery_app.task()
def parse_celery(key: str):
    headers = {'accept': 'application/json'}
    data = {"key": key}
    response = requests.post(parser_url, headers=headers, params=data)
    time.sleep(5)
    return {"status": response.status_code, "response_msg": response.json()['message']}