import typing as tp
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TaskStatusCRUD(BaseModel):
    status: str


class TaskCRUD(TaskStatusCRUD):
    name: str
    description: tp.Optional[str]
    due_date: tp.Optional[datetime]
    assignee_id: tp.Optional[int]


class Task(TaskCRUD):
    id: int
    project_id: tp.Optional[int]

    model_config = ConfigDict(from_attributes=True)
