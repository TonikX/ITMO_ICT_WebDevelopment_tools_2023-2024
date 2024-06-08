from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing_extensions import List, TypedDict

from auth import AuthHandler
from connection import get_session
from exceptions.forbbiden_exception import ForbiddenException
from exceptions.invalid_password_exception import InvalidPasswordException
from exceptions.user_not_found_exception import UserNotFoundException
from exceptions.username_already_registered_exception import UsernameAlreadyRegisteredException
from models.user_models import *
from models.user_models import User
from models.user_trip_link_models import UserTripLinkTrips, UserTripLinkUsers

user_router = APIRouter(tags=["User"])
auth_handler = AuthHandler()


@user_router.get("/user/all", response_model=List[User])
def user_list(session: Session = Depends(get_session)) -> Sequence[User]:
    users = session.exec(select(User)).all()
    return users


@user_router.get("/user/me")
def user_me(session=Depends(get_session),
            current=Depends(auth_handler.current_user)) -> UserDefault:
    user = session.get(User, current.id)
    if not user:
        raise UserNotFoundException
    user_model = user.model_dump(exclude={'password'})
    return UserDefault.model_validate(user_model)


@user_router.get("/user/{user_id}")
def user(user_id: str, session: Session = Depends(get_session)) -> UserDefault:
    user = session.exec(select(User).filter(User.id == user_id)).first()
    return user


@user_router.post("/user/create")
def create(user_data: UserInput, session: Session = Depends(get_session)) -> TypedDict('Response', {"status": int,
                                                                                                    "data": User}):
    db_user = session.exec(select(User).filter(User.username == user_data.username)).first()

    if db_user:
        raise UsernameAlreadyRegisteredException()

    user_data = user_data.model_dump(exclude={'password2'}, exclude_unset=True)
    hashed_pwd = auth_handler.get_hash(user_data.get('password'))
    user_data['password'] = hashed_pwd

    user = User.model_validate(user_data)
    print("user", user)
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"status": 200, "data": user}


@user_router.post("/user/login")
def user_login(user_login: UserLogin, session=Depends(get_session)) -> TypedDict('Response', {"access_token": str,
                                                                                              "token_type": str}):
    print("user_login", user_login)
    user_data = user_login.model_dump(exclude_unset=True)
    found_user = session.exec(select(User).where(User.username == user_data.get('username'))).first()
    if not found_user:
        raise UserNotFoundException
    verified = auth_handler.verify(user_data.get('password'), found_user.password)
    if not verified:
        raise InvalidPasswordException

    token = auth_handler.encode_token(found_user.id)

    print("token", token)
    return {"access_token": token, "token_type": "bearer"}


@user_router.patch("/user/me/pwd")
def user_change_password(user_pwd: UserPwd, session=Depends(get_session),
                         current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                               "message": str}):
    found_user = session.get(User, current.id)
    if not found_user:
        raise UserNotFoundException
    verified = auth_handler.verify(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = auth_handler.get_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}


@user_router.patch("/user/update/{user_id}")
def user_update(user_id: int, user: UserDefault,
                session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> UserDefault:
    db_user = session.get(User, user_id)
    if not db_user:
        raise UserNotFoundException
    if not (user_id == current.id or current.is_admin):
        raise ForbiddenException
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    user_model = db_user.model_dump(exclude={'password'})
    return UserDefault.model_validate(user_model)


@user_router.delete("/user/delete/{user_id}")
def user_delete(user_id: int,
                session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                      "message": str}):
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException
    if not (user_id == current.id or current.is_admin):
        raise ForbiddenException
    session.delete(user)
    session.commit()
    return {"status": 201, "message": f"deleted user with id {user_id}"}
