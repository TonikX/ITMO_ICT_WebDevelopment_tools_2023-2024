"""API задач хакатона (публикация задач организаторами)."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_role
from app.models import Hackathon, Task, User, UserRole
from app.schemas import TaskCreate, TaskOut

router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.post("", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organizer)),
):
    """Публикация задачи (только организатор)."""
    hackathon = db.query(Hackathon).filter(Hackathon.id == data.hackathon_id).first()
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Хакатон не найден"
        )
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("", response_model=List[TaskOut])
def list_tasks(
    hackathon_id: int = Query(None, description="Фильтр по хакатону"),
    db: Session = Depends(get_db),
):
    """Список задач, опционально по конкретному хакатону."""
    query = db.query(Task)
    if hackathon_id is not None:
        query = query.filter(Task.hackathon_id == hackathon_id)
    return query.all()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return task
