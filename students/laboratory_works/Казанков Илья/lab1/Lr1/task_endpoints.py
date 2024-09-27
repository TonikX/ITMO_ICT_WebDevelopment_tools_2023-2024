from fastapi import APIRouter, HTTPException, Depends
from models import Task, TaskBase, TaskShow, User, TaskCategory
from database import get_session
from typing import Optional, List

from sqlmodel import select
from fastapi import APIRouter
from models import Task, TaskBase, TaskShow, User
from typing_extensions import TypedDict
import datetime
from fastapi import HTTPException, Depends
from database import get_session

task_router = APIRouter()


@task_router.post("/tasks/create")
def task_create(task: TaskBase, user_id: int, session=Depends(get_session)):
def task_create(task: TaskBase, user_id: int, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Task}):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    task = Task(**task.dict(), user_id=user_id)
    task = Task.model_validate(task)
    task.user_id = user_id
    session.add(task)
    session.commit()
    session.refresh(task)
    return {"status": 200, "data": task}

@task_router.get("/tasks/list")
def task_list(session=Depends(get_session)) -> list[Task]:
    return session.query(Task).all()

@task_router.post("/tasks/categories/create")
def create_category(name: str, description: str = "", task_ids: Optional[List[int]] = None,session=Depends(get_session)):
    category = TaskCategory(name=name, description=description)
    session.add(category)
    session.commit()

    if task_ids:
        tasks = session.exec(select(Task).where(Task.id.in_(task_ids))).all()
        for task in tasks:
            task.category_id = category.id
            session.add(task)

    session.commit()
    session.refresh(category)
    return {"status": "Category created", "data": category}


@task_router.post("/tasks/assign-to-user")
def assign_tasks_to_user(user_id: int, task_ids: List[int], session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    tasks = session.exec(select(Task).where(Task.id.in_(task_ids))).all()
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")

    for task in tasks:
        task.user_id = user_id
        session.add(task)

    session.commit()
    return {"status": "Tasks assigned to user", "task_ids": task_ids, "user_id": user_id}

@task_router.get("/tasks/{task_id}", response_model=TaskShow)
def task_get(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@task_router.patch("/tasks/update/{task_id}")
def task_update(task_id: int, task: TaskBase, category_id: Optional[int] = None, session=Depends(get_session)):
def task_update(task_id: int, task: TaskBase, session=Depends(get_session)) -> Task:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.dict(exclude_unset=True)
    task_data = task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    if category_id:
        category = session.get(TaskCategory, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        db_task.category_id = category_id

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@task_router.patch("/tasks/update-time-status/{task_id}")
def update_task_time_status(task_id: int, time_spent: int, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
@task_router.delete("/tasks/delete/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.time_spent += time_spent

    db_task.status = True

    session.add(db_task)
    session.delete(task)
    session.commit()
    session.refresh(db_task)
    return {"status": 200, "message": "Task updated", "data": db_task}


@task_router.get("/tasks/list")
def task_list(session=Depends(get_session)):
    return session.query(Task).all()

    return {"ok": True}

@task_router.get("/tasks/{task_id}")
def task_get(task_id: int, session=Depends(get_session)):
@task_router.patch("/tasks/time-spent/{task_id}")
def update_time_spent(task_id: int, time_spent: int, session=Depends(get_session)) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

    task.time_spent += time_spent

@task_router.delete("/tasks/delete/{task_id}")
def task_delete(task_id: int, session=Depends(get_session)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    if datetime.datetime.now() >= task.date_end and not task.status:
        task.status = True

    session.add(task)
    session.commit()
    return {"ok": True}
    session.refresh(task)
    return task