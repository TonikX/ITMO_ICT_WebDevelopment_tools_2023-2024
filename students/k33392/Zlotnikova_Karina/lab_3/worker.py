import asyncio
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.vinil_models import Vinil
from parsing.parser import parse_and_save


import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")

broker = f'redis://{REDIS_HOST}:{REDIS_PORT}'
worker = Celery('tasks', broker=broker)

DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
db_session = Session()

@worker.task(name='Parse')
def parse(url: str):
    asyncio.run(parse_and_save(url, DB_URL))

