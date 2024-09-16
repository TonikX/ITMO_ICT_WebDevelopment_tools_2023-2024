from celery import Celery
from parser.parse_utils import parse, save

celery_app = Celery(
    "tasks", broker="redis://redis:6379/0", backend="redis://redis:6379/0"
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task
def celery_parse_and_save(url):
    data = parse(url)
    save(data)
    print(f"Saved currency: {data['name']}")
