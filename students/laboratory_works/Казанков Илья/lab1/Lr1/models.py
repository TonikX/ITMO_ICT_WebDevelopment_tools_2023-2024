from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from typing import Optional, List
import datetime
from enum import Enum

class TaskPriority(Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    tasks: List["Task"] = Relationship(back_populates="category")

class TaskBase(SQLModel):
    title: str
    description: str
    date_start: datetime.date
    date_end: datetime.date
    date_start: datetime.datetime
    date_end: datetime.datetime
    priority: TaskPriority = TaskPriority.medium
    time_spent: Optional[int] = 0

class TaskShow(TaskBase):
    status: Optional[bool] = False

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message: str
    task_id: int = Field(foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="notifications")
    user_id: int = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="notifications")
    is_read: bool = Field(default=False)

class TaskUserLink(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    status: Optional[bool] = False

    users: List["User"] = Relationship(back_populates="tasks", link_model=TaskUserLink)
    category_id: Optional[int] = Field(default=None, foreign_key="taskcategory.id")
    category: Optional["TaskCategory"] = Relationship(back_populates="tasks")

    notifications: List["Notification"] = Relationship(back_populates="task")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: list['User'] = Relationship(back_populates="tasks")

class UserBase(SQLModel):
    username: str
class UserShow(UserBase):

class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="users", link_model=TaskUserLink)
    notifications: List["Notification"] = Relationship(back_populates="user")
    tasks: Optional[List["Task"]] = Relationship(back_populates="user")

class ChangePassword(SQLModel):
    old_password: str
    new_password: str