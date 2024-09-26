from fastapi import APIRouter, HTTPException
from fastapi import Depends
from models import UserBase, UserShow, User
from connection import get_session
from sqlmodel import select
from typing_extensions import TypedDict

user_router = APIRouter()

@user_router.get("/user-list")
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.exec(select(User)).all()
    return users

@user_router.get("/user/{userId}", response_model= User)
def getUserById(user_id: int, session = Depends(get_session)) -> UserShow:
    obj = session.get(User, user_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="User not found")
    return obj

@user_router.delete("/users/delete/{travel_id}")
def traveltogether_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
