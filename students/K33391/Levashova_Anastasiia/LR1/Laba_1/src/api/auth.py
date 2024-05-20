from connection import get_session
from fastapi import APIRouter, status
from typing import Annotated
from fastapi import Depends, HTTPException
from models import User, Token
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from services.auth import authenticate, create_access_token, get_current_user


router = APIRouter()


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = authenticate(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/getCurrentUser", status_code=status.HTTP_200_OK)
async def get_current_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    return current_user
