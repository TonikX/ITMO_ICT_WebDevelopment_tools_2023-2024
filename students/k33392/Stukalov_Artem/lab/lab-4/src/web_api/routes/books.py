from fastapi import APIRouter, Depends, HTTPException, status
from src.web_api.models import (
    Book,
    BookCreate,
    User,
    BookUpdateStatus,
    BookCreateOwned,
    BookParseByUrl,
)
from src.web_api.config import db
from src.web_api.services import books as books_service, auth as auth_service
from src.web_api.config.env import BOOKS_SEARCH_COUNT_DEFAULT
from sqlmodel import Session
from typing import List
from src.url_parser.main import parse_book
from celery.result import AsyncResult

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def search_books(
    session: Session = Depends(db.get_session),
    query: str = "",
    offset: int = 0,
    count: int = BOOKS_SEARCH_COUNT_DEFAULT,
) -> List[Book]:
    books = books_service.search_books(session, query, offset, count)
    return books


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_book(
    book_create: BookCreate,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
):
    created_book = books_service.create_book(session, book_create, current_user.id)
    return created_book


@router.get("/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: int, session: Session = Depends(db.get_session)):
    book = books_service.get_book_by_id(session=session, id=book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", status_code=status.HTTP_200_OK)
def update_book_status(
    book_id: int,
    book_update: BookUpdateStatus,
    session: Session = Depends(db.get_session),
    _current_user: User = Depends(auth_service.get_current_admin_user),
):
    updated_book = books_service.update_book_status(
        session=session, id=book_id, status=book_update.moderation_status
    )
    return updated_book


@router.post("/owned", status_code=status.HTTP_200_OK)
def create_owned_book(
    book_create: BookCreateOwned,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
) -> bool:
    updated = books_service.add_owned_book(
        session=session, book_id=book_create.book_id, user=current_user
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Failed to add book")

    return updated


@router.post("/parse", status_code=status.HTTP_200_OK)
async def parse_book_by_url(
    book_parse: BookParseByUrl,
    current_user: User = Depends(auth_service.get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not admin")

    task = parse_book.delay(book_parse.url)
    result = AsyncResult(task.id)

    try:
        res = result.get()
        return {"result": res}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
