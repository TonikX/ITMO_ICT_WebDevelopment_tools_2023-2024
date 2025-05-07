from enum import Enum
from sqlmodel import DateTime, SQLModel, Field, Relationship, Column
from datetime import datetime
from typing import List, Optional
import pytz

tz = pytz.UTC

class Priority(Enum):
    high = 1
    medium = 2
    low = 3

class UserDefault(SQLModel):
    name: str
    email: str

class User(UserDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    tasks: List["Task"] = Relationship(back_populates="user")
    hashed_password: str

class TaskCategory(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)

class CategoryDefault(SQLModel):
    name: str

class Category(CategoryDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    name: str
    tasks: List["Task"] = Relationship(back_populates="categories", link_model=TaskCategory)

class TaskDefault(SQLModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    scheduled_datetime: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))
    priority: Priority = Priority.medium

class Task(TaskDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    user_id: int = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="tasks")
    categories: List[Category] = Relationship(back_populates="tasks", link_model=TaskCategory)
    time_logs: List["TaskTimeLog"] = Relationship(back_populates="task")

class TaskTimeLogDefault(SQLModel):
    start_time: datetime = Field(sa_column=Column(DateTime(timezone=True)))
    end_time: Optional[datetime] = Field(default=datetime.now().astimezone(tz), sa_column=Column(DateTime(timezone=True)))

class TaskTimeLog(TaskTimeLogDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    task_id: int = Field(foreign_key="task.id")
    task: Task = Relationship(back_populates="time_logs")
    time_spent: float
