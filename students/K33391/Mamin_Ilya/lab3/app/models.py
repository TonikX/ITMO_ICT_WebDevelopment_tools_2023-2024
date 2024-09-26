import datetime
from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Priority(Enum):
    high = "high"
    medium = "medium"
    low = "low"
    no_priority = "no_priority"


class TaskDefault(SQLModel):
    title: str
    description: Optional[str] = None
    deadline: datetime.date
    priority: Priority = Priority.no_priority
    user_id: int = Field(default=None, foreign_key="user.id")


class TaskShow(TaskDefault):
    title: str
    deadline: datetime.date
    priority: Priority
    time_spent: Optional[int] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: Optional[int] = None
    user: Optional["User"] = Relationship(back_populates="tasks")
    schedules: Optional[List["Schedule"]] = Relationship(back_populates="task")
    reminders: Optional[List["Reminder"]] = Relationship(back_populates="task")


class ScheduleDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class ScheduleShow(ScheduleDefault):
    task: Optional["Task"] = None


class Schedule(ScheduleDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task: Optional["Task"] = Relationship(back_populates="schedules")
    user: Optional["User"] = Relationship(back_populates="schedules")


class ReminderDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    remind_at: datetime.datetime
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class ReminderShow(ReminderDefault):
    task: Optional[Task] = None


class UserBase(SQLModel):
    username: str
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    schedules: Optional[List["Schedule"]] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )
    reminders: Optional[List["Reminder"]] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"}
    )


class Reminder(ReminderDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    task: Optional["Task"] = Relationship(back_populates="reminders")
    user: Optional[User] = Relationship(back_populates="reminders")


class UserShow(UserBase):
    id: int
    tasks: Optional[List["Task"]] = None
    schedules: Optional[List["Schedule"]] = None
    reminders: Optional[List["Reminder"]] = None


class ChangePassword(SQLModel):
    old_password: str
    new_password: str

class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    url: str
    text: str