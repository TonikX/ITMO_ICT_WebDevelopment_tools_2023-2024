from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select, SQLModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from conn import get_session, init_db
from models import * 
from typing import List

from pydanticModels import *

router = APIRouter()



@router.post("/task_categories/")
def create_task_category(task_category_data: TaskCategoryCreate, session: Session = Depends(get_session)):
    task_category = TaskCategory(**task_category_data.dict())
    session.add(task_category)
    session.commit()
    session.refresh(task_category)
    return task_category


@router.get("/task_categories/", response_model=List[TaskCategory])
def read_task_categories(session: Session = Depends(get_session)):
    task_categories = session.query(TaskCategory).all()
    return task_categories




@router.put("/task_categories/{task_id}/{category_id}", response_model=TaskCategoryUpdate)
def update_task_category(task_id: int, category_id: int, task_category_update: TaskCategory, session: Session = Depends(get_session)):
    db_task_category = session.get(TaskCategory, {'task_id': task_id, 'category_id': category_id})
    if not db_task_category:
        raise HTTPException(status_code=404, detail="TaskCategory not found")
    
    db_task_category.additional_info = task_category_update.additional_info

    session.commit()
    return db_task_category

