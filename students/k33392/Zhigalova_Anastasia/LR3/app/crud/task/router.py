from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import Task
from db import get_session

from pydanticModels import *

router = APIRouter()


@router.post("/tasks/", response_model=Task)
def create_task(task: Task, session: Session = Depends(get_session)):
    db_task = Task.from_orm(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/tasks/", response_model=List[Task])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.execute(select(Task)).scalars().all()
    return tasks

@router.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_data: Task, session: Session = Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_data.dict(exclude_unset=True)

    if 'user_id' in update_data and update_data['user_id'] is None:
        raise HTTPException(status_code=400, detail="user_id cannot be null")

    for key, value in update_data.items():
        setattr(db_task, key, value)
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    
    return db_task

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    timelogs = session.query(TimeLog).filter(TimeLog.task_id == task_id).all()
    for timelog in timelogs:
        session.delete(timelog)

    for task_category in task.task_categories: 
        session.delete(task_category)

    session.delete(task)
    session.commit()
    return {"ok": True}