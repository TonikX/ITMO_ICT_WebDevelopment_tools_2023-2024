from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select, Session

from connection import get_session
from models import Book, User, BookCopy, UserOut, UserIn

router = APIRouter(prefix="/book_copy", tags=["Book copy"])


@router.get("", response_model=List[BookCopy])
def get_all_book_copies(session: Session = Depends(get_session)):
    return session.exec(select(BookCopy)).all()


@router.get("/{user_id}/{book_id}", response_model=List[BookCopy])
def get_book_copy_id(user_id: int, book_id: int, session: Session = Depends(get_session)):
    book_copies = session.exec(
        select(BookCopy)
        .where(BookCopy.user_id == user_id)
        .where(BookCopy.book_id == book_id)
    )
    return book_copies
