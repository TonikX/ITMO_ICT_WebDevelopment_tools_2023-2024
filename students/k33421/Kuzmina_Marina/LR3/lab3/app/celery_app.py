from celery import Celery
import requests

celery_app = Celery(
    "tasks",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def parse_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return {"url": url, "status_code": response.status_code}
