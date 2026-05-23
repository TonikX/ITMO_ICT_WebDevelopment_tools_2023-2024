from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_current_user
from app.db.session import get_session
from app.models.schedule import Schedule, ScheduleTaskLink
from app.models.task import Task
from app.models.user import User
from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleRead,
    ScheduleReadDetailed,
    ScheduleTaskItemRead,
    ScheduleTaskLinkCreate,
    ScheduleTaskLinkUpdate,
    ScheduleUpdate,
)
from app.schemas.task import TaskRead

router = APIRouter(prefix="/schedules", tags=["schedules"])


def _get_user_schedule(session: Session, schedule_id: int, user_id: int) -> Schedule:
    schedule = session.exec(
        select(Schedule).where(Schedule.id == schedule_id, Schedule.user_id == user_id)
    ).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule


def _build_schedule_details(session: Session, schedule: Schedule) -> ScheduleReadDetailed:
    # достаем link записи отдельно, чтобы вернуть и задачу, и поля связи в одном ответе
    links = session.exec(
        select(ScheduleTaskLink).where(ScheduleTaskLink.schedule_id == schedule.id)
    ).all()
    items: list[ScheduleTaskItemRead] = []
    for link in sorted(links, key=lambda value: value.sort_order):
        task = session.get(Task, link.task_id)
        if not task:
            continue
        items.append(
            ScheduleTaskItemRead(
                task=TaskRead.model_validate(task),
                planned_start=link.planned_start,
                planned_minutes=link.planned_minutes,
                sort_order=link.sort_order,
            )
        )
    return ScheduleReadDetailed(**ScheduleRead.model_validate(schedule).model_dump(), items=items)


@router.get("", response_model=list[ScheduleRead])
def list_schedules(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[ScheduleRead]:
    items = session.exec(select(Schedule).where(Schedule.user_id == current_user.id)).all()
    return [ScheduleRead.model_validate(item) for item in items]


@router.get("/{schedule_id}", response_model=ScheduleReadDetailed)
def get_schedule(
    schedule_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ScheduleReadDetailed:
    schedule = _get_user_schedule(session, schedule_id, current_user.id)
    return _build_schedule_details(session, schedule)


@router.post("", response_model=ScheduleRead, status_code=status.HTTP_201_CREATED)
def create_schedule(
    payload: ScheduleCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ScheduleRead:
    schedule = Schedule.model_validate(payload, update={"user_id": current_user.id})
    session.add(schedule)
    session.commit()
    session.refresh(schedule)
    return ScheduleRead.model_validate(schedule)


@router.patch("/{schedule_id}", response_model=ScheduleRead)
def update_schedule(
    schedule_id: int,
    payload: ScheduleUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ScheduleRead:
    schedule = _get_user_schedule(session, schedule_id, current_user.id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(schedule, key, value)
    session.add(schedule)
    session.commit()
    session.refresh(schedule)
    return ScheduleRead.model_validate(schedule)


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, bool]:
    schedule = _get_user_schedule(session, schedule_id, current_user.id)
    session.delete(schedule)
    session.commit()
    return {"ok": True}


@router.post("/{schedule_id}/tasks", response_model=ScheduleReadDetailed)
def add_task_to_schedule(
    schedule_id: int,
    payload: ScheduleTaskLinkCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ScheduleReadDetailed:
    schedule = _get_user_schedule(session, schedule_id, current_user.id)
    task = session.exec(select(Task).where(Task.id == payload.task_id, Task.user_id == current_user.id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    existing = session.get(ScheduleTaskLink, (schedule.id, task.id))
    if existing:
        raise HTTPException(status_code=400, detail="Task already in schedule")
    link = ScheduleTaskLink(
        schedule_id=schedule.id,
        task_id=task.id,
        planned_start=payload.planned_start,
        planned_minutes=payload.planned_minutes,
        sort_order=payload.sort_order,
    )
    session.add(link)
    session.commit()
    return _build_schedule_details(session, schedule)


@router.patch("/{schedule_id}/tasks/{task_id}", response_model=ScheduleReadDetailed)
def update_schedule_item(
    schedule_id: int,
    task_id: int,
    payload: ScheduleTaskLinkUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ScheduleReadDetailed:
    schedule = _get_user_schedule(session, schedule_id, current_user.id)
    link = session.get(ScheduleTaskLink, (schedule.id, task_id))
    if not link:
        raise HTTPException(status_code=404, detail="Schedule task link not found")
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(link, key, value)
    session.add(link)
    session.commit()
    return _build_schedule_details(session, schedule)


@router.delete("/{schedule_id}/tasks/{task_id}", response_model=ScheduleReadDetailed)
def remove_task_from_schedule(
    schedule_id: int,
    task_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ScheduleReadDetailed:
    schedule = _get_user_schedule(session, schedule_id, current_user.id)
    link = session.get(ScheduleTaskLink, (schedule.id, task_id))
    if not link:
        raise HTTPException(status_code=404, detail="Schedule task link not found")
    session.delete(link)
    session.commit()
    return _build_schedule_details(session, schedule)
