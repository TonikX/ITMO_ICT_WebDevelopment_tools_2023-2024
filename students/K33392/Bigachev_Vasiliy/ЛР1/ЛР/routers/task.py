from fastapi import APIRouter, Depends
from db import get_session
from typing import List, NotRequired
from typing_extensions import TypedDict
from sqlmodel import select
from models.task import *

router = APIRouter()


@router.get("/task")
def tasks_get(session = Depends(get_session)) -> List[Task]:
    statement = select(Task).order_by(Task.id)
    return session.exec(statement).all()


@router.get("/task/{task_id}")
def task_get(task_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[TaskOut]}):
    task = session.get(Task, task_id)
    if not task:
        return {"status": 404}
    return {"status": 200, "data": task}


@router.post("/task")
def task_post(task: TaskDefault, session = Depends(get_session)):
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 201, "data": task}


@router.put("/task/{task_id}")
def task_update(task: TaskDefault, task_id:int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Task]}):
    task_to_update = session.get(Task, task_id)
    if not task_to_update:
        return {"status": 404}
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task_to_update, key, value)
    session.add(task_to_update)
    session.commit()
    session.refresh(task_to_update)
    return {"status": 201, "data": task_to_update}


@router.delete("/task/{task_id}")
def task_delete(task_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Task]}):
    task_to_delete = session.get(Task, task_id)
    if not task_to_delete:
        return {"status": 404}
    session.delete(task_to_delete)
    session.commit()
    return {"status": 201, "data": task_to_delete}
