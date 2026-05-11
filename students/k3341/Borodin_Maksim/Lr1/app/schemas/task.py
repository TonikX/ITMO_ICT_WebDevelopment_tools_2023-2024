from datetime import datetime

from sqlmodel import SQLModel

from app.models.task import TaskStatus
from app.schemas.priority import PriorityRead


class TimeTrackCreate(SQLModel):
    task_id: int
    started_at: datetime
    ended_at: datetime | None = None
    duration_seconds: int | None = None
    comment: str | None = None


class TimeTrackUpdate(SQLModel):
    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration_seconds: int | None = None
    comment: str | None = None


class TimeTrackRead(SQLModel):
    id: int
    task_id: int
    started_at: datetime
    ended_at: datetime | None = None
    duration_seconds: int | None = None
    comment: str | None = None


class TaskCreate(SQLModel):
    priority_id: int | None = None
    title: str
    description: str | None = None
    deadline_at: datetime | None = None
    status: TaskStatus = TaskStatus.todo


class TaskUpdate(SQLModel):
    priority_id: int | None = None
    title: str | None = None
    description: str | None = None
    deadline_at: datetime | None = None
    status: TaskStatus | None = None


class TaskRead(SQLModel):
    id: int
    user_id: int
    priority_id: int | None = None
    title: str
    description: str | None = None
    deadline_at: datetime | None = None
    status: TaskStatus
    created_at: datetime


class TaskReadDetailed(TaskRead):
    priority: PriorityRead | None = None
    time_tracks: list[TimeTrackRead] = []
