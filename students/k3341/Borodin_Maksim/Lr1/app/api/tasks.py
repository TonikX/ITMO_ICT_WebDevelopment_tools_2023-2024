from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.priority import Priority
from app.models.task import Task, TimeTrack
from app.models.user import User
from app.schemas.priority import PriorityRead
from app.schemas.task import (
    TaskCreate,
    TaskRead,
    TaskReadDetailed,
    TaskUpdate,
    TimeTrackRead,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def list_tasks(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[TaskRead]:
    tasks = session.exec(select(Task).where(Task.user_id == current_user.id)).all()
    return [TaskRead.model_validate(task) for task in tasks]


@router.get("/{task_id}", response_model=TaskReadDetailed)
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TaskReadDetailed:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    priority: Priority | None = None
    if task.priority_id is not None:
        priority = session.get(Priority, task.priority_id)
    time_tracks = session.exec(select(TimeTrack).where(TimeTrack.task_id == task.id)).all()

    return TaskReadDetailed(
        **TaskRead.model_validate(task).model_dump(),
        priority=PriorityRead.model_validate(priority) if priority else None,
        time_tracks=[TimeTrackRead.model_validate(track) for track in time_tracks],
    )


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    task = Task.model_validate(payload, update={"user_id": current_user.id})
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskRead.model_validate(task)


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TaskRead:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return TaskRead.model_validate(task)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    task = session.exec(
        select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
