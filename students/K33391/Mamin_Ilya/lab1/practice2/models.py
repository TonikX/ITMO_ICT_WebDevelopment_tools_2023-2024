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


class TaskShow(TaskDefault):
    title: str
    deadline: datetime.date
    priority: Priority
    time_spent: Optional[int] = None


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    time_spent: Optional[int] = None
    schedules: Optional[List["Schedule"]] = Relationship(back_populates="task")
    reminders: Optional[List["Reminder"]] = Relationship(back_populates="task")


class ScheduleDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    date: datetime.date
    start_time: datetime.time
    end_time: datetime.time


class ScheduleShow(ScheduleDefault):
    task: Optional["Task"] = None


class Schedule(ScheduleDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task: Optional["Task"] = Relationship(back_populates="schedules")


class ReminderDefault(SQLModel):
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    remind_at: datetime.datetime


class ReminderShow(ReminderDefault):
    task: Optional[Task] = None


class Reminder(ReminderDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="reminders")
