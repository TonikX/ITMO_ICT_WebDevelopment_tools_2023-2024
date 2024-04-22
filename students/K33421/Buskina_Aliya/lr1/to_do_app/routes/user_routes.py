from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.exceptions import RequestValidationError
import jwt
from sqlalchemy.orm import Session
import crud, schemas
#from auth import auth
from connection import get_session
from schemas import *
#import auth.auth

router = APIRouter()


@router.post("/users/",
             response_model=UserRead,
             status_code=status.HTTP_201_CREATED,
             tags=["Users"],  # Теги для организации в документации
             summary="Create a new user",  # Краткое описание метода
             description="Create a new user with the provided data.",
             responses={  # Примеры ответов
                 201: {"description": "User created successfully"},
                 400: {"description": "Invalid data provided"},
                 409: {"description": "User with this username already exists"},
                 500: {"description": "Internal server error"},
             }
             )
def create_user(user_data: UserCreate, db: Session = Depends(get_session)):
    return crud.create_user(db=db, **user_data.dict())  # Распаковываем данные из схемы UserCreate

@router.get("/users/{user_id}", response_model=UserRead)  # Указываем, что возвращаемая модель - UserRead
def read_user(user_id: int, db: Session = Depends(get_session)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.put("/users/{user_id}", response_model=UserRead)  # Указываем, что возвращаемая модель - UserRead
def update_user(user_id: int, user_data: UserUpdate, db: Session = Depends(get_session)):
    return crud.update_user(db=db, user_id=user_id, **user_data.dict(exclude_unset=True))  # Распаковываем данные из схемы UserUpdate, исключая пустые значения

@router.delete("/users/{user_id}", response_model=UserRead)  # Указываем, что возвращаемая модель - UserRead
def delete_user(user_id: int, db: Session = Depends(get_session)):
    return crud.delete_user(db=db, user_id=user_id)

@router.get("/users/", response_model=UserList)
def read_users(db: Session = Depends(get_session)):
    users = crud.get_all_users(db)
    return {"users": users}

@router.get("/user/{user_id}/tasks-with-time-logs", response_model=TaskWithTimeLogsList)
def read_user_tasks_with_time_logs(user_id: int, db: Session = Depends(get_session)):
    tasks_with_time_logs = crud.get_user_tasks_with_time_logs(db, user_id)
    if not tasks_with_time_logs:
        raise HTTPException(status_code=404, detail="User has no tasks")
    return {"tasks": tasks_with_time_logs}
