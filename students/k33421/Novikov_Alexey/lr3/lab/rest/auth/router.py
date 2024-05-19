from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from db.database import DatabaseSession
from rest.auth.schemas import Token, User, UserCreateData, UserPassword
from rest.auth.utils import (
    authenticate_user,
    create_access_token,
    create_user,
    get_users,
    CurrentUser,
    get_password_hash,
)

OAuth2Form = Annotated[OAuth2PasswordRequestForm, Depends()]

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token")
async def login_for_access_token(session: DatabaseSession, form_data: OAuth2Form) -> Token:
    user = authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.security.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@router.post("/users", response_model=User)
async def register_user(session: DatabaseSession, user_data: UserCreateData):
    user = create_user(session=session, user_data=user_data)
    session.commit()
    return user


@router.get("/users", response_model=list[User])
async def read_users(session: DatabaseSession):
    return [User.model_validate(user) for user in get_users(session=session)]


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: CurrentUser):
    return current_user


@router.post("/users/change_password/", response_model=User)
async def read_users_me(session: DatabaseSession, current_user: CurrentUser, user_data: UserPassword):
    current_user.hashed_password = get_password_hash(user_data.password)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user
