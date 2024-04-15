from sqlalchemy.orm import Session
import models
import schemas
from passlib.context import CryptContext
import secrets
import hashlib
from fastapi import HTTPException
from starlette import status
import jwt
from datetime import datetime, timedelta
from typing import Optional

# Некоторые секретные ключи для подписи токена
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Функция для создания JWT-токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Хеширование пароля с использованием соли и перца
def hash_password(password: str):
    salt = secrets.token_hex(16)  # Генерация случайной соли
    pepper = "secret_pepper"  # Замените это на свой секретный "перец"
    hash_str = hashlib.sha256((password + salt + pepper).encode()).hexdigest()  # Хэширование пароля с "перцем и солью"
    return salt + hash_str  # Сохраняем соль вместе с хэшем

# Проверка пароля
def verify_password(plain_password: str, hashed_password: str):
    salt = hashed_password[:32]  # Получаем соль из сохраненного хэша
    pepper = "secret_pepper"  # Замените это на свой секретный "перец"
    hash_str = hashlib.sha256((plain_password + salt + pepper).encode()).hexdigest()  # Хэширование введенного пароля с "перцем и солью"
    return hashed_password[32:] == hash_str  # Проверяем совпадение хэшей


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = hash_password(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def change_password(db: Session, user: schemas.User, new_password: schemas.UserPasswordChange):
    if not verify_password(new_password.old_password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password",
        )
    hashed_password = hash_password(new_password.new_password)
    user.hashed_password = hashed_password
    db.commit()
    return {"message": "Password updated successfully"}

def create_trip(db: Session, trip: schemas.TripCreate, user_id: int):
    db_trip = models.Trip(**trip.dict(), user_id=user_id)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


def get_trips(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Trip).offset(skip).limit(limit).all()


def search_partners(db: Session, trip_id: int):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        return None
    return trip.partners


def send_partnership_request(db: Session, trip_id: int, user_id: int):
    partnership_request = models.PartnershipRequest(trip_id=trip_id, user_id=user_id)
    db.add(partnership_request)
    db.commit()
    db.refresh(partnership_request)
    return partnership_request


def get_partnership_requests(db: Session, user_id: int):
    return db.query(models.PartnershipRequest).filter(models.PartnershipRequest.user_id == user_id).all()


def respond_to_partnership_request(db: Session, request_id: int, is_accepted: bool):
    partnership_request = db.query(models.PartnershipRequest).filter(models.PartnershipRequest.id == request_id).first()
    if not partnership_request:
        return None
    if is_accepted:
        # Handle partnership request acceptance logic here
        pass
    else:
        # Handle partnership request rejection logic here
        pass
    return partnership_request