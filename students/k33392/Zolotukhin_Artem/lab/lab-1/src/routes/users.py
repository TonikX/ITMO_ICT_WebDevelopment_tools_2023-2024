from fastapi import APIRouter, status, Depends, HTTPException
from typing import Annotated
from src.models import User, UserCreate, Token, UserGetWithRelations, UserChangePassword
from src.config import db
from src.services import users as users_service, auth as auth_service
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from src.routes import wishlists


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


@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(
    change_password: UserChangePassword,
    session: Session = Depends(db.get_session),
    current_user: User = Depends(auth_service.get_current_user),
) -> bool:
    success = users_service.change_password(
        session=session, user=current_user, old_password=change_password.old_password, new_password=change_password.new_password
    )
    if not success:
        raise HTTPException(status_code=400, detail="Invalid old password")
    return success

router.include_router(wishlists.router, prefix="/wishlists", tags=["wishlists"])
