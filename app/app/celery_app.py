from celery import Celery

celery_app = Celery(
    "fastapi",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/1"
)

celery_app.conf.beat_schedule = {
    "run-parsing-every-2-minutes": {
        "task": "app.tasks.run_periodic_parsing",
        "schedule": 120.0,
    },
}

celery_app.autodiscover_tasks(["app"])
