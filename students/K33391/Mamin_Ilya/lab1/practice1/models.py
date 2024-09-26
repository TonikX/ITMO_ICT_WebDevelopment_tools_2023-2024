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
    id: Optional[int] = Field(default=None, primary_key=True) 
    time_spent: Optional[int] = None

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime.date
    priority: str = "no_priority"
    time_spent: Optional[int] = None