import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery('celery_app', broker=os.getenv('REDIS_HOST', 'redis://localhost:6379/0'),
             backend=os.getenv('REDIS_HOST', 'redis://localhost:6379/0'), include=['celery_backend.tasks'])
