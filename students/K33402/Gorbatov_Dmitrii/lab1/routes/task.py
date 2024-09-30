from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Task

router = APIRouter()

@router.get("/taks_list", response_model=List[Task], tags=["task"])
def task_list(session=Depends(get_session)) -> List[Task]:
    return session.exec(select(Task)).all()

@router.get("/task/{task_id}", response_model=Task, tags=["task"])
def task_read(task_id: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/task/{task_id}", response_model=Task, tags=["task"])
def task_update(task_id: int, task: Task, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.dict(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/task/{task_id}", tags=["task"])
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}

@router.post("/task", response_model=Task, tags=["task"])
def task_create(task: Task, session=Depends(get_session)) -> Task:
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
