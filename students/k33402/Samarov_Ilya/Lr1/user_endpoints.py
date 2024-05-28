from fastapi import APIRouter
from auth import *
from database import get_session
from models import UserBase, User, UserShow
from sqlmodel import select


user_router = APIRouter()

@user_router.get("/users/list")
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.exec(select(User)).all()
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return user_models


@user_router.get("/users/{user_id}")
def user_get(user_id: int, session=Depends(get_session)) -> UserShow:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@user_router.delete("/users/delete/{travel_id}")
def traveltogether_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
