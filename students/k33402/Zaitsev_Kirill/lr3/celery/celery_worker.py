from celery_app import celery_app
from dotenv import load_dotenv
import os

if __name__ == '__main__':
    load_dotenv()
    celery_app.broker_transport_options = {os.getenv("CELERY_REDIS_URL")}
    celery_app.start()
