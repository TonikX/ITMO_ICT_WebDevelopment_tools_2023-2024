from fastapi import FastAPI, Depends, HTTPException
import threading
from sqlalchemy.orm import Session
from .models import *
from .connection import init_db, get_session
from sqlalchemy.orm import joinedload
from .async_parser import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def main():
    return "Main page"


@app.post("/parse_books")
def parse(session: Session = Depends(get_session)):
    urls = fetch_random_book_ids(20)
    threads = []
    for url in urls:
        thread = threading.Thread(target=parse_and_save, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


@app.post("/celery_parse_books")
def parse_books(session: Session = Depends(get_session)):
    urls = fetch_random_book_ids(20)
    for url in urls:
        celery_parse_and_save.delay(url)
    return {"message": "Parsing started"}


@app.get("/books/", response_model=List[BookResponse])
def get_books(session: Session = Depends(get_session)):
    books = session.query(Book).options(joinedload(Book.genres)).all()

    return books
