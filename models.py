from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import date, datetime
from passlib.context import CryptContext


# Enum для приоритета и статуса задач
class PriorityEnum(str, Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class StatusEnum(str, Enum):
    to_do = "To do"
    in_progress = "In progress"
    done = "Done"


# Базовая модель для Category
class CategoryDefault(SQLModel):
    title: str
    description: Optional[str] = ""


# Расширенная модель для Category
class Category(CategoryDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="category")


class TaskTagLink(SQLModel, table=True):
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)
    task_id: int = Field(foreign_key="task.id", primary_key=True)


class TagDefault(SQLModel):
    name: str


class Tag(TagDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTagLink)


# Модель для Task
class TaskDefault(SQLModel):
    title: str
    description: str
    deadline: date
    created_date: date = Field(default_factory=date.today)
    priority: PriorityEnum
    status: StatusEnum
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    category: Optional[Category] = Relationship(back_populates="tasks")
    tags: List[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)
    user: Optional["User"] = Relationship(back_populates="tasks")
    task_time: Optional["TaskTime"] = Relationship(back_populates="task")


class TaskResponse(TaskDefault, table=False):
    id: int
    tags: List["Tag"] = []

    class Config:
        orm_mode = True


# Модель для отслеживания времени выполнения задачи
class TaskTime(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    task_id: Optional[int] = Field(default=None, foreign_key="task.id")
    task: Optional["Task"] = Relationship(back_populates="task_time")


# Базовая модель для User
class UserDefault(SQLModel):
    username: str
    password: Optional[str]
    email: str
    registration_date: date = Field(default_factory=date.today)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Модель пользователя с хэшированием паролей и связью с задачами
class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    hashed_password: str = None
    tasks: List["Task"] = Relationship(back_populates="user")


class Token(SQLModel):
    access_token: str
    token_type: str
