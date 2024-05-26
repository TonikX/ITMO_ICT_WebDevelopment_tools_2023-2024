from fastapi import APIRouter, status
from typing import Annotated
from fastapi import Depends, HTTPException
from src.web_api.models import User, UserCreate, Token, UserGetWithRelations
from src.web_api.config import db
from src.web_api.services import users as users_service, auth as auth_service
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from src.web_api.routes import wishlists


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(
    user_create: UserCreate, session: Session = Depends(db.get_session)
) -> User:
    user = users_service.create_user(session=session, user_create=user_create)
    return user


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(db.get_session),
) -> Token:
    user = users_service.authenticate(
        session=session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = auth_service.create_access_token(user.id)
    return Token(access_token=access_token, token_type="bearer")


@router.get("/getSelf", status_code=status.HTTP_200_OK)
async def get_self_user(
    current_user: Annotated[User, Depends(auth_service.get_current_user)]
) -> UserGetWithRelations:
    return current_user  # type: ignore


router.include_router(wishlists.router, prefix="/wishlists", tags=["wishlists"])
