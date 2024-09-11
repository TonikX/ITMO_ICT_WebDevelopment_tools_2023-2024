import asyncio

import celery

from . import config
from .services import parse

app = celery.Celery('queue', broker=config.redis.dsn, backend=config.redis.dsn)


@app.task
def upload_new_projects(page: int) -> int:
    return asyncio.run(parse.upload_new_projects(page))
