from datetime import timedelta

from connection import get_session
from fastapi import APIRouter, status
from typing import Annotated, List
from fastapi import Depends, HTTPException
from models import User, Token, Task
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from services.auth import authenticate, create_access_token, get_current_user
from sqlmodel import select


router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/login", status_code=status.HTTP_202_ACCEPTED)
def login_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    user = authenticate(
        username=form_data.username, password=form_data.password, session=session
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/getCurrentUser", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/getCurrentUserTasks", response_model=List[Task])
async def get_user_tasks(
        current_user: Annotated[User, Depends(get_current_user)],
        session=Depends(get_session)
) -> List[Task]:
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    tasks_query = select(Task).where(Task.user_id == current_user.id)
    tasks = session.exec(tasks_query).all()
    return tasks
