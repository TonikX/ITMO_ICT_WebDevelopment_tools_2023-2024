from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from conn import get_session, init_db
from models import * 
from typing import List
from sqlalchemy.orm import joinedload

from pydanticModels import *

router = APIRouter()


@router.get("/categories/{category_id}/tasks", response_model=List[Task])
def read_tasks_by_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    tasks = session.query(Task).join(TaskCategory).filter(TaskCategory.category_id == category_id).all()
    return tasks

@router.get("/tasks/{task_id}/categories", response_model=List[Category])
def read_categories_by_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    categories = session.query(Category).join(TaskCategory).filter(TaskCategory.task_id == task_id).all()
    return categories

@router.get("/usersall/", response_model=List[UserWithTaskNames])
def read_users_with_tasks(session: Session = Depends(get_session)):
    statement = select(User).options(joinedload(User.tasks)).distinct()
    result = session.execute(statement)
    users = result.scalars().unique().all()
    users_with_task_names = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "tasks": [{"title": task.title} for task in user.tasks]
        }
        users_with_task_names.append(UserWithTaskNames(**user_data))

    return users_with_task_names
