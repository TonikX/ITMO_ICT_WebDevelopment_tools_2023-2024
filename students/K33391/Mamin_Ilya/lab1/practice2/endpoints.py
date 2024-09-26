import datetime
from fastapi import APIRouter, HTTPException, Depends
from models import Task, TaskDefault
from db import get_session
from sqlmodel.sql.expression import select

app_router = APIRouter()

@app_router.post("/create_task", tags=["tasks"])
def create_task(task: Task, session=Depends(get_session)):
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}

@app_router.put("/update_task/{task_id}", tags=["tasks"])
def update_task(task_id: int, task: TaskDefault, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        return {'status': 404, 'data': 'Task not found'}
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@app_router.delete("/delete_task/{task_id}", tags=["tasks"])
def delete_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return {'status': 404, 'data': 'Task not found'}
    session.delete(task)
    session.commit()
    return {"ok": True}

@app_router.get("/task", tags=["tasks"])
def get_all_tasks(session=Depends(get_session)):
    tasks = session.exec(select(Task)).all()
    if not tasks:
        return {'status': 404, 'data': 'No tasks found'}
    return tasks

@app_router.get("/task/{task_id}", tags=["tasks"])
def get_task(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return {'status': 404, 'data': 'Task not found'}
    return task

@app_router.get("/tasks/{task_id}/time", tags=["tasks"])
def get_task_time(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return {'status': 404, 'data': 'Task not found'}
    return {"time_spent": task.time_spent}

@app_router.put("/tasks/{task_id}/time", tags=["tasks"])
def track_time_spent(task_id: int, time_spent: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        return {'status': 404, 'data': 'Task not found'}
    task.time_spent = time_spent
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
