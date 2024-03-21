import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from lab1.prac2.db.enums import Priority, Status, LinkStatus


class MessageResponse(BaseModel):
    status: int
    message: str


class BaseDataResponse(BaseModel):
    status: int
    data: Any


class NotFoundDataResponse(BaseDataResponse):
    data: str


class TaskLinkDataResponse(BaseDataResponse):
    data: "TaskLinkResponse"


class SprintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    start_at: datetime.datetime
    end_at: datetime.datetime


class TaskLinkBodySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    parent_task_id: int
    child_task_id: int

    status: LinkStatus


class TaskLinkUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    status: LinkStatus


class TaskLinkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    child_task: "TaskResponse"
    status: LinkStatus
    parent_task: "TaskResponse"


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

    sprint: SprintResponse | None
