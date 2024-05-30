from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db.models import Task as TaskModel
from rest.dependencies import DatabaseSession
from rest.tasks.schemas import Task, TaskCreateData, TaskUpdateData

router = APIRouter()


@router.get("/")
def get_tasks(session: DatabaseSession) -> list[Task]:
    stmt = select(TaskModel)
    return session.scalars(stmt).all()


@router.get("/{task_id}")
def get_task(task_id: int, session: DatabaseSession) -> Task:
    stmt = select(TaskModel).where(TaskModel.id == task_id)
    return session.scalars(stmt).first()


@router.post("/")
def create_task(task_data: TaskCreateData, session: DatabaseSession) -> Task:
    task_model = TaskModel.model_validate(task_data)
    session.add(task_model)
    session.commit()
    session.refresh(task_model)

    return task_model


@router.patch("/{task_id}")
def update_task(task_id: int, task_data: TaskUpdateData, session: DatabaseSession) -> Task:
    stmt = select(TaskModel).where(TaskModel.id == task_id)
    task_model = session.scalars(stmt).first()

    for key, value in task_data.model_dump(exclude_unset=True).items():
        setattr(task_model, key, value)

    session.add(task_model)
    session.commit()
    session.refresh(task_model)

    return task_model


@router.delete("/{task_id}")
def delete_task(task_id: int, session: DatabaseSession) -> str:
    stmt = select(TaskModel).where(TaskModel.id == task_id)
    task_model = session.scalars(stmt).first()
    if not task_model:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task_model)
    session.commit()

    return f"Task {task_model.title} deleted"