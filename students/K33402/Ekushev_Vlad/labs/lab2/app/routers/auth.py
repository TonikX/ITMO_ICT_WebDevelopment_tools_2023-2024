from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.core import db
from app.core.config import settings
from app.models.healthcheck import Healthcheck
import app.services.auth as auth_service
from starlette import status

router = APIRouter()


@router.get("/login")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(db.get_session),
) -> Healthcheck:
    user = auth_service.authenticate_user(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        user.username, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")
