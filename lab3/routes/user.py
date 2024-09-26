from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import User

router = APIRouter()

@router.get("/users", response_model=List[User], tags=["user"])
def get_users(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()

@router.get("/users/{user_id}", response_model=User, tags=["user"])
def get_user(user_id: int, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/users", response_model=User, tags=["user"])
def create_user(user: User, session=Depends(get_session)) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.patch("/users/{user_id}", response_model=User, tags=["user"])
def update_user(user_id: int, user: User, session=Depends(get_session)) -> User:
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

@router.delete("/users/{user_id}", tags=["user"])
def delete_user(user_id: int, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}
