from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from lab1.TeamTinder.connection import get_session
from lab1.TeamTinder.models import *


router = APIRouter()


@router.post("/task")
def task(task: TaskDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task}):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}


@router.get("/task/list", response_model=List[TaskExtended])
def teask_list(session=Depends(get_session)) -> List[Task]:
    return session.exec(select(Task)).all()


@router.get("/task/{task_id}", response_model=TaskExtended)
def task_read(task_id: int, session=Depends(get_session)) -> Task:
    return session.get(Task, task_id)


@router.patch("/task/{task_id}")
def task_update(task_id: int, task: TaskPartialUpdate, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/task/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(TeamProject, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
