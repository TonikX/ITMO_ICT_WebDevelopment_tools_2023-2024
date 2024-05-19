import datetime
from enum import StrEnum

from pydantic import BaseModel


class Priority(StrEnum):
    trivial = "trivial"
    blocker = "blocker"
    critical = "critical"
    major = "major"
    minor = "minor"


class Status(StrEnum):
    open = "open"
    in_progress = "in_progress"
    done = "done"


class LinkStatus(StrEnum):
    is_blocked_by = "is_blocked_by"
    blocks = "blocks"


class Sprint(BaseModel):
    id: int
    title: str
    start_at: datetime.datetime
    end_at: datetime.datetime


class Link(BaseModel):
    task: "Task"
    status: LinkStatus


class Task(BaseModel):
    id: int
    summary: str
    priority: Priority
    description: str | None = None
    planned_end_at: datetime.datetime | None = None
    status: Status
    created_at: datetime.datetime
    updated_at: datetime.datetime
    sprint: Sprint | None = None


class TaskWithLinks(Task):
    linked_tasks: list[Link] | None = []


class Message(BaseModel):
    status: int
    message: str


class Data(BaseModel):
    status: int
    data: Task
