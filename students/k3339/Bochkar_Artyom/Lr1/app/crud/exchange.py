from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app import models, schemas
from sqlmodel import Session, select

from app.db.conection import get_session
from app.schemas import schemas
from app.models import models


router = APIRouter()


@router.get("/exchange-requests", response_model=List[schemas.ExchangeRequestWithDetails])
def get_all_exchange_requests(session: Session = Depends(get_session)):
  requests = session.exec(select(models.ExchangeRequest)).all()
  return requests


@router.get("/exchange-request/{request_id}", response_model=schemas.ExchangeRequestWithDetails)
def get_exchange_request(request_id: int, session: Session = Depends(get_session)):
  request = session.get(models.ExchangeRequest, request_id)
  if not request:
    raise HTTPException(status_code=404, detail="Заявка не найдена")
  return request


@router.put("/exchange-request/{request_id}", response_model=schemas.ExchangeRequestRead)
def update_exchange_request(
    request_id: int,
    request_update: schemas.ExchangeRequestUpdate,
    session: Session = Depends(get_session)
):
  db_request = session.get(models.ExchangeRequest, request_id)
  if not db_request:
    raise HTTPException(status_code=404, detail="Заявка не найдена")

  db_request.status = request_update.status
  session.add(db_request)
  session.commit()
  session.refresh(db_request)
  return db_request


@router.get("/profile/{profile_id}/sent-requests", response_model=List[schemas.ExchangeRequestWithDetails])
def get_sent_requests(profile_id: int, session: Session = Depends(get_session)):
  profile = session.get(models.Profile, profile_id)
  if not profile:
    raise HTTPException(status_code=404, detail="Пользователь не найден")

  return profile.sent_requests


@router.get("/profile/{profile_id}/received-requests", response_model=List[schemas.ExchangeRequestWithDetails])
def get_received_requests(profile_id: int, session: Session = Depends(get_session)):
  profile = session.get(models.Profile, profile_id)
  if not profile:
    raise HTTPException(status_code=404, detail="Пользователь не найден")

  requests = session.exec(
    select(models.ExchangeRequest)
    .join(models.Book)
    .where(models.Book.owner_id == profile_id)
  ).all()

  return requests


@router.get("/book/{book_id}/requests", response_model=List[schemas.ExchangeRequestWithDetails])
def get_book_requests(book_id: int, session: Session = Depends(get_session)):
  book = session.get(models.Book, book_id)
  if not book:
    raise HTTPException(status_code=404, detail="Книга не найдена")

  return book.requests


@router.delete("/exchange-request/{request_id}")
def delete_exchange_request(request_id: int, session: Session = Depends(get_session)):
  request = session.get(models.ExchangeRequest, request_id)
  if not request:
    raise HTTPException(status_code=404, detail="Заявка не найдена")

  session.delete(request)
  session.commit()
  return {"message": "Заявка удалена успешно"}