from datetime import date
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class Status(Enum):
    to_do = "To do"
    in_progress = "In progress"
    blocked = 'Blocked'
    done = "Done"


class Priority(Enum):
    high = "High"
    medium = "Medium"
    low = 'Low'


class Category(BaseModel):
    id: int
    title: str
    description: str


class Note(BaseModel):
    id: int
    content: str
    created_at: date = date.today()


class Task(BaseModel):
    id: int
    title: str
    description: str
    deadline: date
    created_date: date = date.today()
    priority: Priority
    status: Status
    category: Category
    notes: Optional[List[Note]] = []
