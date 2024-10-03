from celery import Celery
from celery.utils.log import get_task_logger
from asynctask import main
import asyncio

logger = get_task_logger(__name__)

celery = Celery('worker', broker='redis://redis:6379')

@celery.task
def parse_and_save(urls):
    logger.info(f"Started task with URLs: {urls}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))
    logger.info(f"Completed task with URLs: {urls}")

@celery.task
def add(x, y):
    return x + y