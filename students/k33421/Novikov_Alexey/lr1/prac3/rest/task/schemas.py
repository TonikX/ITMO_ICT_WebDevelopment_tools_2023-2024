import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from ...db.enums import Priority, Status, LinkStatus


class MessageResponse(BaseModel):
    status: int
    message: str


class BaseDataResponse(BaseModel):
    status: int
    data: Any


class NotFoundDataResponse(BaseDataResponse):
    data: str


class TaskDataResponse(BaseDataResponse):
    data: "TaskResponse"


class TaskWithLinksDataResponse(BaseDataResponse):
    data: "TaskWithLinksResponse"


class SprintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    start_at: datetime.datetime
    end_at: datetime.datetime


class TaskLinkBaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    child_task: "TaskResponse"
    status: LinkStatus


class TaskBodySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    summary: str
    priority: Priority
    description: str | None
    planned_end_at: datetime.datetime | None
    status: Status
    sprint_id: int | None


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


class TaskWithLinksResponse(TaskResponse):
    linked_tasks: list[TaskLinkBaseResponse] | None
