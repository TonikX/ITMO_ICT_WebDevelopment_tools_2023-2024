from datetime import date, datetime, time

from sqlmodel import SQLModel

from app.schemas.task import TaskRead


class ScheduleCreate(SQLModel):
    schedule_date: date
    title: str = "daily plan"


class ScheduleUpdate(SQLModel):
    schedule_date: date | None = None
    title: str | None = None


class ScheduleRead(SQLModel):
    id: int
    user_id: int
    schedule_date: date
    title: str
    created_at: datetime


class ScheduleTaskLinkCreate(SQLModel):
    task_id: int
    planned_start: time | None = None
    planned_minutes: int = 30
    sort_order: int = 0


class ScheduleTaskLinkUpdate(SQLModel):
    planned_start: time | None = None
    planned_minutes: int | None = None
    sort_order: int | None = None


class ScheduleTaskItemRead(SQLModel):
    task: TaskRead
    planned_start: time | None = None
    planned_minutes: int
    sort_order: int


class ScheduleReadDetailed(ScheduleRead):
    items: list[ScheduleTaskItemRead] = []
