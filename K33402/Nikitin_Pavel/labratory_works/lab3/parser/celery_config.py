from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

app = Celery('tasks', broker=redis_url, backend=redis_url)

app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()