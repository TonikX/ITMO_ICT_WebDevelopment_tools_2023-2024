from celery_app import celery_app
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    redis_url = os.getenv("CELERY_REDIS_URL")
    celery_app.broker_transport_options = {redis_url}
    celery_app.start()
