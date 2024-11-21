from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import date, datetime


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


# Базовая модель для Task
class TaskDefault(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    deadline: date
    created_date: date = Field(default_factory=date.today)
    priority: PriorityEnum
    status: StatusEnum
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")


# Расширенная модель для Task
class Task(TaskDefault, table=True):
    tags: List[Tag] = Relationship(back_populates="tasks", link_model=TaskTagLink)

    # Добавляем связь с Category
    category: Optional[Category] = Relationship(back_populates="tasks")

