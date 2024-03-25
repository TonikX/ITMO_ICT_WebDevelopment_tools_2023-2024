import hmac
import os
from binascii import unhexlify
from datetime import datetime, timedelta, timezone
from hashlib import sha512
from http import HTTPStatus

import jwt
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from conn import get_session
from models import User

from .models import TokenCreate, TokenCreateResponse

router = APIRouter(prefix="/auth")


@router.post("")
def generate_token(data: TokenCreate, session: Session = Depends(get_session)) -> TokenCreateResponse:
    if (user := session.exec(select(User).where(User.email == data.email)).one()) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "User was not found")
    if not hmac.compare_digest(sha512(data.password.encode()).digest(), unhexlify(user.password_hash.encode())):
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
    iat = datetime.now(tz=timezone.utc)
    return {
        "token": jwt.encode(
            {"sub": data.email, "exp": int((iat + timedelta(minutes=15)).timestamp()), "iat": int(iat.timestamp())},
            os.getenv("JWT_KEY"),
        )
    }
