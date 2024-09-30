from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import User

router = APIRouter()

@router.get("/user/list", response_model=List[User], tags=["user"])
def user_list(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()

@router.get("/user/{user_id}", response_model=User, tags=["user"])
def user_read(user_id: int, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/user/{user_id}", response_model=User, tags=["user"])
def user_update(user_id: int, user: User, session=Depends(get_session)) -> User:
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.delete("/user/{user_id}", tags=["user"])
def user_delete(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
