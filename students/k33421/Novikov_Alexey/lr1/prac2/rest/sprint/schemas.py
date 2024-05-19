import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from lab1.prac2.db.enums import Priority, Status


class MessageResponse(BaseModel):
    status: int
    message: str


class BaseDataResponse(BaseModel):
    status: int
    data: Any


class NotFoundDataResponse(BaseDataResponse):
    data: str


class SprintDataResponse(BaseDataResponse):
    data: "SprintResponse"


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    summary: str
    priority: Priority
    description: str | None
    planned_end_at: datetime.datetime | None
    status: Status
    created_at: datetime.datetime
    updated_at: datetime.datetime


class SprintBodySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    start_at: datetime.datetime
    end_at: datetime.datetime


class SprintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    start_at: datetime.datetime
    end_at: datetime.datetime

    tasks: list[TaskResponse]
