from celery import Celery
import asyncio
from parser import main_start

app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@app.task
def parse_urls():
    asyncio.run(main_start())
