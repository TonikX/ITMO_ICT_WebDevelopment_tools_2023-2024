from celery import Celery
import requests

app = Celery('tasks', broker='redis://redis:6379')

@app.task
def db_parse_celery(urls, num):
    params = {'num': f'{num}'}
    response = requests.post('http://parser:8010/parse', params=params, json=urls)
    return response.json()