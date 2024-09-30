from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str
    password: Optional[str] = None
    hashed_password: str
    task_infos: List["TaskInfo"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    task_infos: List["TaskInfo"] = Relationship(back_populates="task")
    tags: List["TaskTagLink"] = Relationship(back_populates="task")
    time_logs: List["TimeLog"] = Relationship(back_populates="task")

class TaskInfo(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    priority: Optional[int] = None
    deadline: Optional[datetime] = None
    task: Task = Relationship(back_populates="task_infos")
    user: User = Relationship(back_populates="task_infos")

class Tag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    tasks: List["TaskTagLink"] = Relationship(back_populates="tag")

class TaskTagLink(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)
    task: Task = Relationship(back_populates="tags")
    tag: Tag = Relationship(back_populates="tasks")

class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    start_time: datetime
    end_time: datetime
    task: Task = Relationship(back_populates="time_logs")

class Site(SQLModel, table=True):
    __tablename__ = "sites"

    id: int = Field(default=None, primary_key=True)
    url: str
    title: str
    method: str

    class Config:
        orm_mode = True
        table_args = {"extend_existing": True}