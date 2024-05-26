from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from typing import Any
from src.web_api.config.env import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from src.web_api.models import User
from typing import Annotated
from fastapi import Depends, HTTPException, status
from src.web_api.services import users as users_service
from src.web_api.config import db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")


def create_access_token(subject: str | Any) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_current_user_id(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if not sub:
            return None
        user_id = int(sub)
        return user_id
    except jwt.JWTError:  # type: ignore
        return None


CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Session = Depends(db.get_session),
) -> User:
    user_id = get_current_user_id(token)
    if not user_id:
        raise CREDENTIALS_EXCEPTION

    user = users_service.get_user_by_id(session=session, id=user_id)
    if not user:
        raise CREDENTIALS_EXCEPTION

    return user


async def get_current_admin_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not admin user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
