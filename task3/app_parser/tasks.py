from celery import Celery
from parser_threading.main import main

celery = Celery('tasks', broker='redis://redis:6379')



@celery.task
def parse_task(token):
    main(token)
