from dotenv import load_dotenv
import os

load_dotenv()

CPU_COUNT = 20
START_ID = 204100
DB_URL = os.getenv("DB_URL") or 'postgresql://postgres:postgres@db:5432/web_data'
DB_URL_ASYNC = os.getenv("DB_URL_ASYNC") or ""
URLS = list(
    [
        f"https://bookcrossing.ru/books/{i}"
        for i in range(START_ID, START_ID + CPU_COUNT)
    ]
)
