from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from app.models.schedule import ScheduleTaskLink

if TYPE_CHECKING:
    from app.models.priority import Priority
    from app.models.schedule import Schedule
    from app.models.user import User


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"


class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    priority_id: int | None = Field(default=None, foreign_key="priorities.id", index=True)
    title: str = Field(max_length=120)
    description: str | None = Field(default=None, max_length=500)
    deadline_at: datetime | None = None
    status: TaskStatus = Field(default=TaskStatus.todo)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="tasks")
    priority: "Priority" = Relationship(back_populates="tasks")
    time_tracks: list["TimeTrack"] = Relationship(back_populates="task")
    schedules: list["Schedule"] = Relationship(
        back_populates="tasks",
        link_model=ScheduleTaskLink,
    )


class TimeTrack(SQLModel, table=True):
    __tablename__ = "time_tracks"

    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="tasks.id", index=True)
    started_at: datetime
    ended_at: datetime | None = None
    duration_seconds: int | None = Field(default=None, ge=0)
    comment: str | None = Field(default=None, max_length=255)

    task: Task = Relationship(back_populates="time_tracks")
