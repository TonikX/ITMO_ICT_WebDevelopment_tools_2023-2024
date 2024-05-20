from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Any, Union
from fastapi.security import OAuth2PasswordBearer
from connection import get_session
from sqlmodel import select

from fastapi import status
from typing import Annotated
from fastapi import Depends, HTTPException
from models import User, Token
from sqlmodel import Session

SECRET_KEY = "MY_TEST_SECRET_KEY"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

def create_access_token(subject: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
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


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(get_session),
) -> User:
    user_id = get_current_user_id(token)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = get_user_by_id(session=session, id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user

def get_user_by_username(session: Session, username: str) -> Union[User, None]:
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    return user


def get_user_by_id(session: Session, id: int) -> Union[User, None]:
    query = select(User).where(User.id == id)
    user = session.exec(query).first()
    return user


def authenticate(session: Session, username: str, password: str) -> Union[User, None]:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
