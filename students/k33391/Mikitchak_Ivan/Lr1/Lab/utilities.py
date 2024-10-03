from dotenv import load_dotenv
import os

from fastapi import HTTPException, status

from sqlmodel import Session, select

from typing import Dict, Optional, Union
from models import User

import jwt
from passlib.context import CryptContext

from datetime import UTC, datetime, timedelta

import string
import random


load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
DEFAULT_EXP_DELTA_MIN = int(os.getenv("DEFAULT_EXP_DELTA_MIN"))


def create_access_token(data: dict, exp_delta: Union[timedelta, None] = None) -> str:
    payload = data.copy()
    iat = datetime.now(UTC)
    if not exp_delta:
        exp = iat + timedelta(minutes=DEFAULT_EXP_DELTA_MIN)
    else:
        exp = iat + exp_delta
    payload.update({"iat": iat, "exp": exp})

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


def validate_access_token(token: str) -> Optional[Dict[str, any]]:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    claims = (isinstance(payload.get("sub"), int) and
              isinstance(payload.get("iat"), int) and
              isinstance(payload.get("exp"), int))

    if not claims:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bad token claims."
        )

    return payload


def get_user_by_token(token: str, session: Session) -> Optional[User]:
    payload = validate_access_token(token)

    user = session.exec(select(User).where(User.id == payload["sub"])).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User claimed by token not found. Most likely the user has been deleted."
        )

    if user.last_logout is not None and datetime.fromtimestamp(payload["iat"], UTC) < user.last_logout:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token was invalidated by user logout."
        )

    return user


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def generate_code(length: int = 8) -> str:
    pool = string.ascii_letters + string.digits
    return "".join(random.choices(pool, k=length))
