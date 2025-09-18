from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app import models, schemas
from sqlmodel import Session, select

from app.db.conection import get_session
from app.schemas import schemas
from app.models import models


router = APIRouter()


@router.get("/profiles", response_model=List[schemas.ProfileRead])
def get_profiles(session: Session = Depends(get_session)):
  profiles = session.exec(select(models.Profile)).all()
  return profiles


@router.get("/profile/{profile_id}", response_model=schemas.ProfileWithBooks)
def get_profile(profile_id: int, session: Session = Depends(get_session)):
  profile = session.get(models.Profile, profile_id)
  if not profile:
    raise HTTPException(status_code=404, detail="Профиль не найден")
  return profile

@router.get("/profile/{profile_id}/books", response_model=List[schemas.BookRead])
def get_books_by_owner(profile_id: int, session: Session = Depends(get_session)):
  owner = session.get(models.Profile, profile_id)
  if not owner:
    raise HTTPException(status_code=404, detail="Владелец не найден")

  books = session.exec(
    select(models.Book).where(models.Book.owner_id == profile_id)
  ).all()
  return books


@router.get("/profile/{profile_id}/with-books", response_model=schemas.ProfileWithBooks)
def get_profile_with_books(profile_id: int, session: Session = Depends(get_session)):
  profile = session.get(models.Profile, profile_id)
  if not profile:
    raise HTTPException(status_code=404, detail="Профиль не найден")

  return profile


@router.patch("/profile/{profile_id}", response_model=schemas.ProfileRead)
def update_profile(
    profile_id: int,
    profile_update: schemas.ProfileUpdate,
    session: Session = Depends(get_session)
):
    db_profile = session.get(models.Profile, profile_id)
    if not db_profile:
        raise HTTPException(status_code=404, detail="Профиль не найден")

    # Проверяем уникальность username только если он меняется
    if profile_update.username and db_profile.username != profile_update.username:
        existing = session.exec(
            select(models.Profile).where(models.Profile.username == profile_update.username)
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Имя пользователя уже занято")

    # Обновляем только переданные поля
    update_data = profile_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_profile, key, value)

    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)
    return db_profile


@router.delete("/profile/{profile_id}")
def delete_profile(profile_id: int, session: Session = Depends(get_session)):
  profile = session.get(models.Profile, profile_id)
  if not profile:
    raise HTTPException(status_code=404, detail="Профиль не найден")

  session.delete(profile)
  session.commit()
  return {"message": "Профиль удален успешно"}