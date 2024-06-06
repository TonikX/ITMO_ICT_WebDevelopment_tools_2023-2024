from celery import Celery

celery_app = Celery(
    "cel_app",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
)

celery_app.conf.update(
    task_routes={
        "parse.parse_and_save": "main-queue",
    },
)

if __name__ == "__main__":
    celery_app.start()