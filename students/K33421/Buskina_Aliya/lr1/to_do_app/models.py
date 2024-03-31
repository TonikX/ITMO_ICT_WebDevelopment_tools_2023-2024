from datetime import datetime, date
from sqlmodel import Field, Relationship, SQLModel
from typing import List, Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    hashed_password: str
    password: Optional[str] = Field(default=None, exclude=True)
    is_active: bool = Field(default=True)
    tasks: List["Task"] = Relationship(back_populates="owner")

class TaskCategory(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    category_id: int = Field(foreign_key="category.id", primary_key=True)
    additional_info: str
    task: "Task" = Relationship(back_populates="task_categories")
    category: "Category" = Relationship(back_populates="category_tasks")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    deadline: Optional[date] = None
    priority: int = Field(default=1)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: User = Relationship(back_populates="tasks")
    task_categories: List[TaskCategory] = Relationship(back_populates="task")
    time_logs: List["TimeLog"] = Relationship(back_populates="task")

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    category_tasks: List[TaskCategory] = Relationship(back_populates="category")

class TimeLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    time_spent_minutes: int
    date_logged: date
    task: Task = Relationship(back_populates="time_logs")

metadata = SQLModel.metadata