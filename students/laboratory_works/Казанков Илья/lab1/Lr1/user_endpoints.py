from fastapi import APIRouter, HTTPException, Depends
from models import User, UserShow, Notification
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from models import UserBase, User, UserShow
from database import get_session
from sqlmodel import select

user_router = APIRouter()


@user_router.get("/users/list")
def user_list(session=Depends(get_session)):
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.exec(select(User)).all()
    user_models = [user.dict(exclude={'password'}) for user in users]
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return user_models


@user_router.get("/users/{user_id}", response_model=UserShow)
def user_get(user_id: int, session=Depends(get_session)):
def user_get(user_id: int, session=Depends(get_session)) -> UserShow:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/users/delete/{user_id}")
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
def user_delete(user_id: int, session=Depends(get_session)):
    session.delete(user)
    session.commit()
    return {"ok": True}


@user_router.get("/users/{user_id}/notifications")
def get_user_notifications(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    notifications = session.exec(select(Notification).where(Notification.user_id == user_id)).all()
    return {"data": notifications}