from dotenv import load_dotenv
import os

load_dotenv()

DB_URL = os.getenv("DB_URL") or  'postgresql://postgres:postgres@db:5432/web_data'
SECRET_KEY = "dsanfsdklf0412lk12je1902oivnervner923hsfdkjdfkjsfhh3k2hfkj2ksfdjkfhsdkfioj3oifj2iojsdhfjkhsdjfhnsbpapczxksjdfbeo"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
BOOKS_SEARCH_COUNT_DEFAULT = 10
