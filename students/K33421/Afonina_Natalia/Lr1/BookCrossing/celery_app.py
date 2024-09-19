from celery import Celery
from celery.utils.log import get_task_logger
from asynctask import main_async
import asyncio

logger = get_task_logger(__name__)

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def parse_and_save_authors_task(urls):
    logger.info(f"Started task with URLs: {urls}")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_async(urls))
    logger.info(f"Completed task with URLs: {urls}")
