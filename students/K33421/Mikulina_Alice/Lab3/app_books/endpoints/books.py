from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlmodel import or_, select, Session
from datetime import datetime
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import joinedload
import requests

from db.models import Book, BookDefault, AppUser, BookGenre, Genre
from connection import get_session
from .auth import get_current_user


class GenreResponse(BaseModel):
    id: int
    name: str

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: str
    condition: str
    user_id: int
    created_at: str
    last_updated_at: str
    genres: List[GenreResponse]

class ParseRequest(BaseModel):
    url: str


router = APIRouter()


@router.get("/search", response_model=list[BookResponse])
def search_books(query: str, session: Session = Depends(get_session)):
    books = (
        session.exec(
            select(Book)
            .options(joinedload(Book.genres))
            .where(
                or_(
                    Book.title.like(f"%{query}%"),
                    Book.author.like(f"%{query}%"),
                    Book.description.like(f"%{query}%")
                )
            )
        )
        .unique()
        .all()
    )

    book_responses = []
    for book in books:
        genres = [GenreResponse(id=genre.id, name=genre.name) for genre in book.genres]
        book_response = BookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            description=book.description,
            condition=book.condition,
            user_id=book.user_id,
            created_at=str(book.created_at),
            last_updated_at=str(book.last_updated_at),
            genres=genres
        )
        book_responses.append(book_response)

    return book_responses


@router.get("/", response_model=list[BookResponse])
def get_books(session: Session = Depends(get_session)):
    books = (
        session.exec(
            select(Book)
            .options(joinedload(Book.genres))
        )
        .unique()
        .all()
    )
    book_responses = []
    for book in books:
        genres = [GenreResponse(id=genre.id, name=genre.name) for genre in book.genres]
        print(genres)
        book_response = BookResponse(
            id=book.id,
            title=book.title,
            author=book.author,
            description=book.description,
            condition=book.condition,
            user_id=book.user_id,
            created_at=str(book.created_at),
            last_updated_at=str(book.last_updated_at),
            genres=genres
        )
        book_responses.append(book_response)

    return book_responses

@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = (
        session.exec(
            select(Book)
            .options(joinedload(Book.genres))
            .where(Book.id == book_id)
        )
        .unique()
        .one_or_none()
    )
    print(book.genres)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("/", response_model=Book)
def create_book(book: BookDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book = Book(
        title=book.title,
        author=book.author,
        description=book.description,
        condition=book.condition,
        user_id=current_user.id,
    )
    session.add(db_book)
    session.commit()
    return db_book


@router.post("/parse", status_code=202)
async def parse_books(request: ParseRequest, current_user: AppUser = Depends(get_current_user), session: Session = Depends(get_session)):
    try:
        response = requests.post(
            "http://parser/parse",
            json={"url": request.url, "user_id": current_user.id}
        )
        response.raise_for_status()
        return {"message": "Books parsing initiated"}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, book: BookDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permision denied")

    # Update the book's attributes
    db_book.title = book.title
    db_book.author = book.author
    db_book.description = book.description
    db_book.condition = book.condition
    db_book.user_id = current_user.id
    db_book.last_updated_at = datetime.now()

    session.add(db_book)
    session.commit()
    return db_book

@router.delete("/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book = session.get(Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    if db_book.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Permision denied")
    
    session.delete(db_book)
    session.commit()
    return {"message": "Book deleted"}