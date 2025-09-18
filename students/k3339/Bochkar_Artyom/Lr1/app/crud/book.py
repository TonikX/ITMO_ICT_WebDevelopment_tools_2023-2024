from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app import models, schemas
from sqlmodel import Session, select

from app.db.conection import get_session
from app.schemas import schemas
from app.models import models


router = APIRouter()


@router.get("/books", response_model=List[schemas.BookRead])
def get_books(session: Session = Depends(get_session)):
  books = session.exec(select(models.Book)).all()
  return books


@router.get("/books/available", response_model=List[schemas.BookRead])
def get_available_books(session: Session = Depends(get_session)):
  books = session.exec(
    select(models.Book).where(models.Book.owner_id == None)
  ).all()
  return books


@router.get("/book/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, session: Session = Depends(get_session)):
  book = session.get(models.Book, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Книга не найдена")
  return book


@router.post("/book", response_model=schemas.BookRead)
def create_book(book: schemas.BookCreate, session: Session = Depends(get_session)):
  if book.owner_id is not None:
    owner = session.get(models.Profile, book.owner_id)
    if not owner:
      raise HTTPException(status_code=404, detail="Владелец не найден")

  db_book = models.Book.model_validate(book)
  session.add(db_book)
  session.commit()
  session.refresh(db_book)
  return db_book

@router.patch("/book/{book_id}", response_model=schemas.BookRead)
def update_book(
    book_id: int,
    book_update: schemas.BookUpdate,
    session: Session = Depends(get_session)
):
    db_book = session.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")

    # Проверяем владельца только если он меняется
    if book_update.owner_id is not None and book_update.owner_id != db_book.owner_id:
        owner = session.get(models.Profile, book_update.owner_id)
        if not owner:
            raise HTTPException(status_code=404, detail="Владелец не найден")

    # Обновляем только переданные поля
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_book, key, value)

    session.add(db_book)
    session.commit()
    session.refresh(db_book)
    return db_book

@router.put("/book/{book_id}/assign", response_model=schemas.BookRead)
def assign_book_to_owner(book_id: int, owner_id: int, session: Session = Depends(get_session)):
  book = session.get(models.Book, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Книга не найдена")

  owner = session.get(models.Profile, owner_id)
  if not owner:
    raise HTTPException(status_code=404, detail="Владелец не найден")

  book.owner_id = owner_id
  session.add(book)
  session.commit()
  session.refresh(book)
  return book


@router.put("/book/{book_id}/release", response_model=schemas.BookRead)
def release_book_from_owner(book_id: int, session: Session = Depends(get_session)):
  book = session.get(models.Book, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Книга не найдена")

  book.owner_id = None
  session.add(book)
  session.commit()
  session.refresh(book)
  return book


@router.delete("/book/{book_id}")
def delete_book(book_id: int, session: Session = Depends(get_session)):
  book = session.get(models.Book, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Книга не найдена")

  active_requests = session.exec(
    select(models.ExchangeRequest).where(
      models.ExchangeRequest.book_id == book_id,
      models.ExchangeRequest.status == models.RequestStatus.PENDING
    )
  ).all()

  if active_requests:
    raise HTTPException(
      status_code=400,
      detail="Нельзя удалить книгу с активными заявками на обмен"
    )

  session.delete(book)
  session.commit()
  return {"message": "Книга удалена успешно"}