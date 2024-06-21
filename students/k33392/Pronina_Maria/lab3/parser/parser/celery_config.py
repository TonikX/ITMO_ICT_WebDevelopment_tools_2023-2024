from celery import Celery
from fastapi import HTTPException
from connection import get_session
from parse import parse_and_save
import requests 

celery_app = Celery("parser", backend='redis://redis:6379/1', broker='redis://redis:6379/0')

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    broker_connection_retry_on_startup=True
)


@celery_app.task
def parsing_task(usernames):
    try:
        session = next(get_session())
        parse_and_save(usernames, session)
        # parse_task.delay(usernames)
        return {"message": "Parsing task started"}
    except requests.RequestException as err:
        raise HTTPException(status_code=500, detail=str(err))
