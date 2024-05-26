Описание используемых моделей
```python
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


class LabelDefault(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    content: Optional[str] = ""
    created_at: date = Field(default_factory=date.today)


class Label(LabelDefault, table=True):
    task_lab: List["Task"] = Relationship(back_populates="label")


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
    time_spent: Optional[float] = None
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    label_id: Optional[int] = Field(default=None, foreign_key="label.id")
    done_date: Optional[date] = None


class Task(TaskDefault, table=True):
    category: Optional[Category] = Relationship(back_populates="task_cat")
    label: Optional[Label] = Relationship(back_populates="task_lab")


class TasksCategories(TaskDefault):
    category: Optional[Category] = None


class TasksLabels(TaskDefault):
    label: Optional[Label] = None

```