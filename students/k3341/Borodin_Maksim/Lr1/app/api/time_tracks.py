from datetime import timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.task import Task, TimeTrack
from app.models.user import User
from app.schemas.task import TimeTrackCreate, TimeTrackRead, TimeTrackUpdate

router = APIRouter(prefix="/time-tracks", tags=["time-tracks"])


def _ensure_task_owner(session: Session, task_id: int, user_id: int) -> Task:
    task = session.exec(select(Task).where(Task.id == task_id, Task.user_id == user_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("", response_model=list[TimeTrackRead])
def list_time_tracks(
    task_id: int | None = None,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[TimeTrackRead]:
    query = select(TimeTrack).join(Task).where(Task.user_id == current_user.id)
    if task_id is not None:
        query = query.where(TimeTrack.task_id == task_id)
    items = session.exec(query).all()
    return [TimeTrackRead.model_validate(item) for item in items]


@router.get("/{track_id}", response_model=TimeTrackRead)
def get_time_track(
    track_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TimeTrackRead:
    item = session.exec(
        select(TimeTrack).join(Task).where(TimeTrack.id == track_id, Task.user_id == current_user.id)
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Time track not found")
    return TimeTrackRead.model_validate(item)


@router.post("", response_model=TimeTrackRead, status_code=status.HTTP_201_CREATED)
def create_time_track(
    payload: TimeTrackCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TimeTrackRead:
    _ensure_task_owner(session, payload.task_id, current_user.id)
    duration = payload.duration_seconds
    # если duration не передали, считаем по времени, чтобы не хранить пустое значение
    if duration is None and payload.ended_at is not None:
        delta = payload.ended_at.astimezone(timezone.utc) - payload.started_at.astimezone(timezone.utc)
        duration = max(int(delta.total_seconds()), 0)
    item = TimeTrack.model_validate(payload, update={"duration_seconds": duration})
    session.add(item)
    session.commit()
    session.refresh(item)
    return TimeTrackRead.model_validate(item)


@router.patch("/{track_id}", response_model=TimeTrackRead)
def update_time_track(
    track_id: int,
    payload: TimeTrackUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> TimeTrackRead:
    item = session.exec(
        select(TimeTrack).join(Task).where(TimeTrack.id == track_id, Task.user_id == current_user.id)
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Time track not found")
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(item, key, value)
    # если обновили границы времени, синхронизируем duration, чтобы аналитика была проще
    if item.started_at and item.ended_at:
        delta = item.ended_at.astimezone(timezone.utc) - item.started_at.astimezone(timezone.utc)
        item.duration_seconds = max(int(delta.total_seconds()), 0)
    session.add(item)
    session.commit()
    session.refresh(item)
    return TimeTrackRead.model_validate(item)


@router.delete("/{track_id}")
def delete_time_track(
    track_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    item = session.exec(
        select(TimeTrack).join(Task).where(TimeTrack.id == track_id, Task.user_id == current_user.id)
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Time track not found")
    session.delete(item)
    session.commit()
    return {"ok": True}
