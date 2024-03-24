from sqlmodel import SQLModel, Field, Relationship
from datetime import date
from typing import Optional, List
from enum import Enum


class StatusEnum(Enum):
    to_do = "To do"
    in_progress = "In progress"
    blocked = "Blocked"
    done = "Done"


class PriorityEnum(Enum):
    high = "High"
    medium = "Medium"
    low = "Low"


class LabelTaskLink(SQLModel, table=True):
    label_id: Optional[int] = Field(
        default=None, foreign_key="label.id", primary_key=True
    )
    task_id: Optional[int] = Field(
        default=None, foreign_key="task.id", primary_key=True
    )


class LabelDefault(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: Optional[str] = ""
    created_at: date = Field(default_factory=date.today)


class Label(LabelDefault, table=True):
    tasks: Optional[List["Task"]] = Relationship(back_populates="labels", link_model=LabelTaskLink)


class CategoryDefault(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: Optional[str] = ""


class Category(CategoryDefault, table=True):
    task_cat: List["Task"] = Relationship(back_populates="category")


class TaskDefault(SQLModel):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    deadline: date
    created_date: date = Field(default_factory=date.today)
    priority: PriorityEnum
    status: StatusEnum
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Task(TaskDefault, table=True):
    category: Optional[Category] = Relationship(back_populates="task_cat")
    labels: Optional[List[Label]] = Relationship(back_populates="tasks", link_model=LabelTaskLink)


class TasksCategories(TaskDefault):
    category: Optional[Category] = None
