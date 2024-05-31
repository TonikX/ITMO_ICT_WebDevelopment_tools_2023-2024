from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlmodel import select, Session
from datetime import datetime

from db.models import BookGenre, BookGenreDefault, AppUser, Book, Genre
from connection import get_session
from .auth import get_current_user

router = APIRouter()

@router.get("/", response_model=list[BookGenre])
def get_booksgenres(session: Session = Depends(get_session)):
    books_genres = session.exec(select(BookGenre)).all()
    return books_genres

@router.get("/{book_genre_id}", response_model=BookGenre)
def get_bookgenre(book_genre_id: int, session: Session = Depends(get_session)):
    book_genre = session.get(BookGenre, book_genre_id)
    if not book_genre:
        raise HTTPException(status_code=404, detail="BookGenre not found")
    return book_genre

@router.post("/", response_model=BookGenre)
def create_bookgenre(book_genre: BookGenreDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    print(book_genre.book_id)
    db_book_genre = BookGenre(
        book_id=book_genre.book_id,
        genre_id=book_genre.genre_id,
    )

    db_book = session.get(Book, db_book_genre.book_id)
    db_genre = session.get(Genre, db_book_genre.genre_id)

    db_book.genres.append(db_genre)
    db_genre.books.append(db_book)

    session.add(db_book)
    session.add(db_genre)
    session.add(db_book_genre)
    session.commit()
    return db_book_genre

@router.put("/{book_genre_id}", response_model=BookGenre)
def update_bookgenre(book_genre_id: int, book_genre: BookGenreDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book_genre = session.get(BookGenre, book_genre_id)
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="BookGenre not found")
    
    # Update the book_genre's attributes
    db_book_genre.book_id = book_genre.book_id
    db_book_genre.genre_id = book_genre.genre_id

    session.add(db_book_genre)
    session.commit()
    return db_book_genre

@router.delete("/{book_genre_id}")
def delete_bookgenre(book_genre_id: int, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book_genre = session.get(BookGenre, book_genre_id)
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="BookGenre not found")
    
    session.delete(db_book_genre)
    session.commit()
    return {"message": "BookGenre deleted"}