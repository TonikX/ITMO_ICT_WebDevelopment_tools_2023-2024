from fastapi import APIRouter, Depends, HTTPException

from auth.auth import AuthHandler
from db import get_session
from typing import List, NotRequired, Union
from typing_extensions import TypedDict
from sqlmodel import select
from models.user import *

router = APIRouter()
auth_handler = AuthHandler()

@router.get("/user")
def projects_get(session=Depends(get_session)) -> List[UserOut]:
    statement = select(User).order_by(User.id)
    return session.exec(statement).all()


@router.post("/user")
def project_post(user: UserDefault, session=Depends(get_session)) -> TypedDict("Response", {"status": int, "data": NotRequired[User]}):
    user = User.model_validate(user)
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"status": 201, "data": user}


@router.put("/user/{user_id}")
def project_put(user: UserDefault, user_id: int, session=Depends(get_session)) -> TypedDict("Response", {"status": int, "data": NotRequired[User]}):
    user_to_update = session.get(User, user_id)
    if not user_to_update:
        return {"status": 404}
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user_to_update, key, value)
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return {"status": 201, "data": user_to_update}


@router.delete("/user/{user_id}")
def task_delete(user_id: int, session=Depends(get_session)) -> TypedDict("Response", {"status": int, "data": NotRequired[User]}):
    user_to_delete = session.get(User, user_id)
    if not user_to_delete:
        return {"status": 404}
    session.delete(user_to_delete)
    session.commit()
    return {"status": 201, "data": user_to_delete}


@router.post("/signup")
def sing_up(user: UserSignUp, session=Depends(get_session)) -> TypedDict("Response", {"status": int, "data": NotRequired[User]}):
    statement = select(User)
    users = session.exec(statement).all()

    if any(x.nickname == user.nickname for x in users):
        return {"status": 400}

    hashed_pwd = auth_handler.get_password_hash(user.password)
    user_to_create = User(nickname=user.nickname, hashed_password=hashed_pwd, email=user.email)
    session.add(user_to_create)
    session.commit()
    return {"status": 201}


@router.post('/signin')
def login(user: UserSignIn, session=Depends(get_session)):
    statement = select(User).where(User.nickname == user.nickname)
    user_found = session.exec(statement).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.hashed_password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.nickname)
    return {'token': token}


@router.get('/user/me')
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user


@router.patch('/user/new-password')
def update_password(new_password: str, user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)):
    if not user:
        raise HTTPException(status_code=401, detail='User is not found')
    new_hashed_password = auth_handler.get_password_hash(new_password)
    user.hashed_password = new_hashed_password
    session.add(user)
    session.commit()
    return {"status": 201}
