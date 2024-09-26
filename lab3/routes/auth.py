import jwt
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, Header
from typing_extensions import Optional
import os
from dotenv import load_dotenv, find_dotenv
from sqlmodel import select
from datetime import datetime, timedelta

from connection import get_session
from models import User


load_dotenv(find_dotenv('..'))
secret_key = os.getenv('SECRET_KEY')


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())


def encode_token(username: str) -> str:
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=12),
        'iat': datetime.utcnow(),
        'sub': username
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_token(token: str) -> str:
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Token expired')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


router = APIRouter()


@router.post("/registration", tags=["auth"])
def registration(user: User, session=Depends(get_session)) -> dict:
    if user.password is None:
        raise HTTPException(status_code=400, detail='Password must be provided')


    user.hashed_password = hash_password(user.password)
    user.password = None 

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"status": 200, "data": user}


@router.post("/login", tags=["auth"])
def login(username: str, password: str, session=Depends(get_session)) -> str:
    query = select(User).where(User.username == username)
    db_user = session.exec(query).one_or_none()
    if not db_user:
        raise HTTPException(status_code=401, detail='Invalid username')

    if not verify_password(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid password')

    token = encode_token(db_user.username)
    return token


@router.get("/user/auth/token", response_model=User, tags=["auth"])
def get_user_by_token(token: Optional[str] = Header(None), session=Depends(get_session)) -> User:
    if not token:
        raise HTTPException(status_code=401, detail='Unauthorized')

    token = token
    user_name = decode_token(token)
    query = select(User).where(User.username == user_name)
    user = session.exec(query).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user