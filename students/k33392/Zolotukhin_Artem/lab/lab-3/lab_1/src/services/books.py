from sqlmodel import Session, select
from src.models import Book, BookCreate, BookModerationStatus, User
from typing import List, Union


def search_books(session: Session) -> List[Book]:
    statement = select(Book)
    results = list(session.exec(statement).all())
    return results


def create_book(session: Session, book_create: BookCreate, user_id: int) -> Book:
    db_book = Book.model_validate(
        book_create,
        update={
            "moderation_status": BookModerationStatus.pending,
            "creator_id": user_id,
        },
    )
    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book


def get_book_by_id(session: Session, id: int) -> Union[Book, None]:
    statement = select(Book).where(Book.id == id)
    user = session.exec(statement).first()
    return user


def update_book_status(
    session: Session, id: int, status: BookModerationStatus
) -> Union[Book, None]:
    book = get_book_by_id(session, id)
    if not book:
        return None

    book.moderation_status = status
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def add_owned_book(session: Session, book_id: int, user: User) -> bool:
    book = get_book_by_id(session, book_id)
    if not book:
        return False

    book.owners.append(user)
    session.add(book)
    session.commit()
    session.refresh(book)
    return True
