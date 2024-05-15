from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing_extensions import List, TypedDict

from auth import AuthHandler
from connection import get_session
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.username_already_registered_exception import UsernameAlreadyRegisteredException
from models.user_models import *
from models.user_models import User

user_router = APIRouter(tags=["User"])
auth_handler = AuthHandler()


@user_router.get("/user/all")
def user_list(session: Session = Depends(get_session)) -> Sequence[User]:
    users = session.exec(select(User)).all()
    return users


@user_router.get("/user/{user_id}")
def user(user_id: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).filter(User.id == user_id)).first()
    return user


@user_router.post("/user/create")
def create(user_data: UserDefault, session: Session = Depends(get_session)):
    db_user = session.exec(select(User).filter(User.username == user_data.username)).first()

    if db_user:
        raise UsernameAlreadyRegisteredException()

    user_data = user_data.model_dump(exclude={'password2'}, exclude_unset=True)
    hashed_pwd = auth_handler.get_hash(user_data.get('password'))
    user_data['password'] = hashed_pwd

    user = User.model_validate(user_data)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"status": 200, "data": user}


@user_router.post("/user/login")
def user_login(user_login: UserLogin, session=Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                              "token": str}):
    user_data = user_login.model_dump(exclude_unset=True)
    found_user = session.exec(select(User).where(User.username == user_data.get('username'))).first()
    if not found_user:
        raise HTTPException(status_code=404, detail="User with this username doesn't exist")
    verified = auth_handler.verify(user_data.get('password'), found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid password")
    token = auth_handler.encode_token(found_user.id)
    return {"status": 200, "token": token}


@user_router.patch("/user/update/{user_id}")
def update(user_id: str, user_dto: UserDefault, session: Session = Depends(get_session)):
    user = session.exec(select(User).filter(User.id == user_id)).first()

    if not user:
        raise UserNotFoundException()

    user = User.model_validate(user_dto)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 200, "data": user}


@user_router.delete("/user/delete/{user_id}")
def delete(user_id: str, session: Session = Depends(get_session)):
    user = session.exec(select(User).filter(User.id == user_id)).first()

    if not user:
        raise UserNotFoundException()

    session.delete(user)
    session.commit()

    return {"status": 200, "data": user}
