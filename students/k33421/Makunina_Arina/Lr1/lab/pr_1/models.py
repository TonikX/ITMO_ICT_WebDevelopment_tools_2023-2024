from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    deadline: datetime
    priority: PriorityLevel
    time_spent: Optional[float] = 0.0


class Schedule(BaseModel):
    date: datetime
    tasks: List[Task]


class TimeAnalysis(BaseModel):
    task_id: int
    time_spent: float


class CreateTask(BaseModel):
    title: str
    description: str
    deadline: datetime
    priority: PriorityLevel


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[PriorityLevel] = None
    time_spent: Optional[float] = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    priority: PriorityLevel
    time_spent: float
