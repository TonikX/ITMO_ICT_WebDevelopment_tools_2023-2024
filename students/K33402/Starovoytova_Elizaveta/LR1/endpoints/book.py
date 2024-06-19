from fastapi import APIRouter, HTTPException
from sqlmodel import select
from fastapi import Depends
from models import Book, BookBase, BookReadFull
from database.conn import get_session

book_router = APIRouter()


@book_router.get("/")
def get_books(session=Depends(get_session)) -> list[BookReadFull] :
    return session.exec(select(Book)).all()


@book_router.get("/{book_id}")
def get_book(book_id: int, session=Depends(get_session)) -> BookReadFull:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@book_router.post("/")
def create_book(book_data: BookBase, session=Depends(get_session)) -> Book:
    book = Book.model_validate(book_data)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book
