from datetime import date, time, datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.task import Task
    from app.models.user import User


class ScheduleTaskLink(SQLModel, table=True):
    __tablename__ = "schedule_task_link"

    schedule_id: Optional[int] = Field(
        default=None,
        foreign_key="schedules.id",
        primary_key=True,
    )
    task_id: Optional[int] = Field(
        default=None,
        foreign_key="tasks.id",
        primary_key=True,
    )
    planned_start: time | None = None
    planned_minutes: int = Field(default=30, ge=1)
    sort_order: int = Field(default=0, ge=0)


class Schedule(SQLModel, table=True):
    __tablename__ = "schedules"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    schedule_date: date
    title: str = Field(default="daily plan", max_length=100)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="schedules")
    tasks: list["Task"] = Relationship(
        back_populates="schedules",
        link_model=ScheduleTaskLink,
    )
