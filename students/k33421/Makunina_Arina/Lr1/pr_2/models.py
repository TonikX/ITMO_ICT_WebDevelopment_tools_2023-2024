from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskScheduleLink(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    schedule_id: int = Field(foreign_key="schedule.id", primary_key=True)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: int
    schedules: List["Schedule"] = Relationship(
        back_populates="tasks", link_model=TaskScheduleLink
    )


class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    tasks: List[Task] = Relationship(
        back_populates="schedules", link_model=TaskScheduleLink
    )


Task.schedules: List[Schedule] = Relationship(
    back_populates="tasks", link_model=TaskScheduleLink
)

Schedule.tasks: List[Task] = Relationship(
    back_populates="schedules", link_model=TaskScheduleLink
)


class TimeAnalysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    time_spent: float
    task: Task = Relationship(back_populates="time_analyses")


Task.time_analyses: List[TimeAnalysis] = Relationship(back_populates="task")


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


class TaskBase(BaseModel):
    title: str
    description: str
    priority: int


class ScheduleBase(BaseModel):
    date: datetime


class ScheduleResponse(ScheduleBase):
    id: int
    tasks: List[TaskResponse]


class TaskResponse(TaskBase):
    id: int
    schedules: List[ScheduleResponse]


class CreateSchedule(ScheduleBase):
    pass
