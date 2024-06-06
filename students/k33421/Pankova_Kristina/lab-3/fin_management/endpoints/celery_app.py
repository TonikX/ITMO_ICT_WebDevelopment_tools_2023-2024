from celery import Celery
import requests

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'


app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.update(from_object='config')

@app.task
def parse_url(url):
    """
    Задача для парсинга URL в фоновом режиме.
    """
    print(f"Parsing URL: {url}")
    url = "http://parser:8001/parse"
    response = requests.post(url, json={"url": url})
    response.raise_for_status()
    return "Parsing completed"
