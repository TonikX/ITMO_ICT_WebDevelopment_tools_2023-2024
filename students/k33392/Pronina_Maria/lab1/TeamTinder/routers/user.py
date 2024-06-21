from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from lab1.TeamTinder.connection import get_session
from lab1.TeamTinder.models import *


router = APIRouter()


@router.get("/user/list", response_model=List[UserExtended])
def user_list(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()


@router.get("/user/{user_id}", response_model=UserExtended)
def user_read(user_id: int, session=Depends(get_session)) -> User:
    return session.get(User, user_id)


@router.get("/user/{user_id}/skills", response_model=List[Skill])
def get_user_skills(user_id: int, session=Depends(get_session)) -> List[Skill]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user.skills


@router.patch("/user/{user_id}", response_model=UserExtended)
def user_update(user_id: int, user: UserPartialUpdate, session=Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/user/{user_id}")
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
