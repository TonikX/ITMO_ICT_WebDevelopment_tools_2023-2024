import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

app = Celery('celery_app', broker=os.getenv('REDIS_HOST'), backend=os.getenv('REDIS_HOST'),
             include=['celery_backend.tasks'])
