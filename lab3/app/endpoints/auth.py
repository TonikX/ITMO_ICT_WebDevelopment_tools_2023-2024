from datetime import timedelta
from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, select
from fastapi.security import OAuth2PasswordRequestForm
from typing import List, Annotated, Sequence

from models import User, Token, Task
from connection import get_session
from service.auth import authenticate, create_access_token, get_current_user

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=Token)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session)
) -> Token:
    # Аутентификация пользователя по его логину и паролю
    user = authenticate(
        username=form_data.username, password=form_data.password, session=session
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # Создание токена доступа
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Получение данных текущего пользователя
@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


# Получение задач текущего пользователя
@router.get("/me/tasks", response_model=List[Task])
async def get_user_tasks(
    current_user: Annotated[User, Depends(get_current_user)],
    session: Session = Depends(get_session)
) -> Sequence[Task]:
    # Проверка существования текущего пользователя
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Получение задач, связанных с пользователем
    tasks_query = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(tasks_query).all()
    return tasks
