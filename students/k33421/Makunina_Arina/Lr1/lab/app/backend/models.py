from enum import Enum
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLAlchemyEnum, String


class PriorityLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class TaskStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    DEFERRED = "deferred"


class TaskScheduleLink(SQLModel, table=True):
    task_id: int = Field(default=None, foreign_key="task.id", primary_key=True)
    schedule_id: int = Field(default=None, foreign_key="schedule.id", primary_key=True)
    assignment_date: datetime = Field(default_factory=datetime.utcnow)
    note: Optional[str] = Field(default=None)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    priority: PriorityLevel = Field(sa_column=Column(SQLAlchemyEnum(PriorityLevel)))
    deadline: datetime
    user_id: int = Field(foreign_key="user.id")
    status: TaskStatus = Field(
        sa_column=Column(SQLAlchemyEnum(TaskStatus)), default=TaskStatus.ACTIVE
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    schedules: List["Schedule"] = Relationship(
        back_populates="tasks", link_model=TaskScheduleLink
    )
    user: Optional["User"] = Relationship(back_populates="tasks")
    time_analyses: List["TimeAnalysis"] = Relationship(back_populates="task")


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, nullable=False)
    email: str = Field(index=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: List[Task] = Relationship(back_populates="user")


class Schedule(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime
    user_id: int = Field(foreign_key="user.id")
    tasks: List["Task"] = Relationship(
        back_populates="schedules", link_model=TaskScheduleLink
    )


Task.schedules = Relationship(back_populates="tasks", link_model=TaskScheduleLink)
Schedule.tasks = Relationship(back_populates="schedules", link_model=TaskScheduleLink)


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
    user_id: int


class UpdateTask(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[PriorityLevel] = None
    time_spent: Optional[float] = None
    user_id: int


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    deadline: datetime
    priority: PriorityLevel
    status: TaskStatus
    user_id: int
    deadline: Optional[datetime] = None
    time_spent: float = 0

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    title: str
    description: str
    priority: int


class ScheduleBase(BaseModel):
    date: datetime

    class Config:
        from_attributes = True


class ScheduleResponse(ScheduleBase):
    id: int
    tasks: List[TaskResponse]


class CreateSchedule(ScheduleBase):
    tasks: List[int]


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserAuthenticate(BaseModel):
    username: str
    password: str


class CreateTimeAnalysis(BaseModel):
    task_id: int
    time_spent: Optional[float] = None


class TimeAnalysisResponse(BaseModel):
    id: int
    task_id: int
    time_spent: float
