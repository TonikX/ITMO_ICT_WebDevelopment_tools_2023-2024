import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class TaskPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"


class TaskBase(SQLModel):
    title: str
    description: str
    date_start: datetime.datetime
    date_end: datetime.datetime
    priority: TaskPriority = TaskPriority.medium
    time_spent: Optional[int] = 0


class TaskShow(TaskBase):
    status: Optional[bool] = False

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[bool] = False
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="tasks")


class UserBase(SQLModel):
    username: str
    password: str


class UserShow(UserBase):
    tasks: Optional[List["Task"]] = None


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="user")  # Связь с задачами


class ChangePassword(SQLModel):
    old_password: str
    new_password: str
