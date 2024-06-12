from celery import Celery
import os

redis_host = os.getenv("REDIS_HOST")
redis_port = os.getenv("REDIS_PORT")
redis_url = f"redis://{redis_host}:{redis_port}"

app = Celery("parser", broker=redis_url, backend=redis_url)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

app.autodiscover_tasks(["parsers.parser"])
