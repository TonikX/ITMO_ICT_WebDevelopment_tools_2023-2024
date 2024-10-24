from hashlib import sha512
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from conn import get_session
from dependencies import verify_jwt
from models import User

from .models import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users")


@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)) -> User:
    user_obj = User(**user.model_dump(), password_hash=sha512(user.password.encode()).hexdigest())
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj


@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(verify_jwt)])
def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    if (user := session.get(User, user_id)) is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get("", dependencies=[Depends(verify_jwt)])
def list_users(session: Session = Depends(get_session)) -> list[User]:
    return session.exec(select(User)).all()


@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(verify_jwt)])
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)) -> User:
    user_obj = session.get(User, user_id)
    if not user_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    user_obj.sqlmodel_update(user.model_dump(exclude_unset=True))
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj


@router.delete("/{user_id}", dependencies=[Depends(verify_jwt)])
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_obj = session.get(User, user_id)
    if not user_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    session.delete(user_obj)
    session.commit()
    return {"message": "User deleted successfully"}
