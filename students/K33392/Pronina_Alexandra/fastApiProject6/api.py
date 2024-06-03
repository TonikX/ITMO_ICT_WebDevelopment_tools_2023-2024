# api.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from starlette import status

import schemas
import crud
from database import SessionLocal
import security

router = APIRouter()

# Функция для получения экземпляра базы данных
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Регистрация пользователя
@router.post("/register/", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)) -> schemas.User:
    return crud.create_user(db=db, user=user)

# Авторизация пользователя и генерация JWT-токена
@router.post("/login/")
def login_user(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)) -> dict:
    user = crud.authenticate_user(db=db, email=user_credentials.email, password=user_credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = crud.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

# Получение информации о текущем пользователе
@router.get("/user/", response_model=schemas.User)
def get_current_user(current_user: schemas.User = Depends(security.get_current_user)) -> schemas.User:
    return current_user

# Получение списка пользователей
@router.get("/users/", response_model=List[schemas.User])
def get_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.User]:
    users = crud.get_users(db=db, skip=skip, limit=limit)
    return users

# Создание поездки
@router.post("/trips/", response_model=schemas.Trip)
def create_trip(trip: schemas.TripCreate, current_user: schemas.User = Depends(security.get_current_user), db: Session = Depends(get_db)) -> schemas.Trip:
    return crud.create_trip(db=db, trip=trip, user_id=current_user.id)

# Получение списка поездок
@router.get("/trips/", response_model=List[schemas.Trip])
def get_trips(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> List[schemas.Trip]:
    trips = crud.get_trips(db=db, skip=skip, limit=limit)
    return trips

# Поиск попутчиков для конкретной поездки
@router.get("/trips/{trip_id}/partners/", response_model=List[schemas.User])
def search_partners(trip_id: int, db: Session = Depends(get_db)) -> List[schemas.User]:
    return crud.search_partners(db=db, trip_id=trip_id)

# Отправка запроса на партнерство для поездки
@router.post("/trips/{trip_id}/partnership/", response_model=schemas.PartnershipRequest)
def send_partnership_request(trip_id: int, current_user: schemas.User = Depends(security.get_current_user), db: Session = Depends(get_db)) -> schemas.PartnershipRequest:
    return crud.send_partnership_request(db=db, trip_id=trip_id, user_id=current_user.id)

# Управление запросами на партнерство для своих поездок
@router.get("/partnership/requests/", response_model=List[schemas.PartnershipRequest])
def get_partnership_requests(current_user: schemas.User = Depends(security.get_current_user), db: Session = Depends(get_db)) -> List[schemas.PartnershipRequest]:
    return crud.get_partnership_requests(db=db, user_id=current_user.id)

# Принятие или отклонение запроса на партнерство
@router.put("/partnership/requests/{request_id}/", response_model=schemas.PartnershipRequest)
def respond_to_partnership_request(request_id: int, is_accepted: bool, db: Session = Depends(get_db)) -> schemas.PartnershipRequest:
    return crud.respond_to_partnership_request(db=db, request_id=request_id, is_accepted=is_accepted)
