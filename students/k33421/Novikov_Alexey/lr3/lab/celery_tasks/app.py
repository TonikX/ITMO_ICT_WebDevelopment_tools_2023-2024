import httpx
from celery import Celery

from config import settings

redis_conf = settings.redis
rabbitmq_conf = settings.rabbitmq

app = Celery(
    "celery_app",
    result_backend=f"redis://{redis_conf.host}:6379/0",
    broker=f"pyamqp://guest@{rabbitmq_conf.host}:5672//",
)


@app.task
def parse_title(url):
    with httpx.Client() as client:
        response = client.get(url)

    title = response.text.split("<title>")[1].split("</title>")[0].strip()

    return {"data": title}
