from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Union
from fastapi.security import OAuth2PasswordBearer
from connection import get_session
from sqlmodel import select

from fastapi import status
from fastapi import Depends, HTTPException
from models import User, Token
from sqlmodel import Session

SECRET_KEY = "MY_TEST_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_current_user_id(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            return None
        user_id = int(sub)
        return user_id
    except jwt.JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: Session = Depends(get_session)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    user = get_user_by_username(username, session=session)
    if user is None:
        raise credential_exception

    return user

def get_user_by_username(username: str, session=Depends(get_session)) -> Union[User, None]:
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    return user


def get_user_by_id(id: int, session=Depends(get_session)) -> Union[User, None]:
    query = select(User).where(User.id == id)
    user = session.exec(query).first()
    return user


def authenticate(username: str, password: str, session=Depends(get_session)) -> Union[User, None]:
    user = get_user_by_username(username, session)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
