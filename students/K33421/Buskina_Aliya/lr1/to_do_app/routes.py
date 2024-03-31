from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud
from connection import get_session
from schemas import *

router = APIRouter()

@router.post("/users/", response_model=UserRead)  # Указываем, что возвращаемая модель - UserRead
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

@router.post("/tasks/", response_model=Task)
def create_task(task_data: TaskCreate, db: Session = Depends(get_session)):
    return crud.create_task(db=db, **task_data.dict())

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.get("/tasks/", response_model=TaskList)
def read_all_tasks(db: Session = Depends(get_session)):
    tasks = crud.get_all_tasks(db)
    return {"tasks": tasks}

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db=db, task_id=task_id, **task_data.dict(exclude_unset=True))

@router.delete("/tasks/{task_id}", response_model=Task)
def delete_task(task_id: int, db: Session = Depends(get_session)):
    db_task = crud.get_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.delete_task(db=db, task_id=task_id)