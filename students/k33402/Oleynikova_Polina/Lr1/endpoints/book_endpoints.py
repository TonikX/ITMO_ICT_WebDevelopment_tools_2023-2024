from fastapi import APIRouter, HTTPException
from sqlmodel import select
from fastapi import Depends
from models import Book, BookBase, BookReadFull
from db.connection import get_session

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


@book_router.patch("/{book_id}")
def update_book(book_id: int, book_data: BookBase, session=Depends(get_session)) -> Book:
    book = session.exec(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for key, value in book_data.model_dump(exclude_unset=True).items():
        setattr(book, key, value)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@book_router.delete("/{book_id}")
def delete_book(book_id: int, session=Depends(get_session)):
    book = session.exec(select(Book).where(Book.id == book_id)).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(book)
    session.commit()
    return {"ok": True}