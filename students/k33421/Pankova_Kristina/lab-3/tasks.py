from celery import Celery
from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
import requests

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
