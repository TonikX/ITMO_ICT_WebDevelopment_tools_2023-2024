from celery import Celery
from db import get_session
from parsing import parse_and_save

celery_app = Celery(
    'parser',
    broker='redis://redis:6379/0',  
    backend='redis://redis:6379/0'  
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)

@celery_app.task
def parse_url_task(url):
    db = next(get_session())
    parsed_data = parse_and_save(db, url)
    return parsed_data