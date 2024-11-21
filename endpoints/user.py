from datetime import date
from typing import List, Optional, Type, Sequence
from fastapi import HTTPException, Depends, APIRouter
from passlib.context import CryptContext
from sqlmodel import select, Session

from models import User, UserDefault, Task
from connection import get_session

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Получить список всех пользователей
@router.get("/")
def get_users(session: Session = Depends(get_session)) -> Sequence[User]:
    return session.exec(select(User)).all()


# Получить конкретного пользователя по его ID
@router.get("/{user_id}", response_model=UserDefault)
def get_user(user_id: int, session: Session = Depends(get_session)) -> Type[User]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Создать нового пользователя
@router.post("/", response_model=UserDefault)
def create_user(user_data: UserDefault, session: Session = Depends(get_session)) -> User:
    hashed_password = pwd_context.hash(user_data.password)
    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


# Обновить информацию о пользователе
@router.patch("/{user_id}", response_model=UserDefault)
def update_user(
        user_id: int,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        session: Session = Depends(get_session)
) -> Type[User]:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.password = user.hash(password)

    session.commit()
    session.refresh(user)
    return user


# Удалить пользователя
@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"status": "User deleted"}


