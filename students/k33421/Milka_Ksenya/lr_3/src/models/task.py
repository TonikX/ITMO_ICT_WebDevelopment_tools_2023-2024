import typing as tp
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from . import mixins

if tp.TYPE_CHECKING:
    from .project import Project
    from .user import User


class Task(mixins.IDMixin, SQLModel, table=True):
    name: str
    description: tp.Optional[str] = None
    status: str
    due_date: tp.Optional[datetime] = None
    project_id: tp.Optional[int] = Field(None, foreign_key="project.id")
    assignee_id: tp.Optional[int] = Field(None, foreign_key="user.id")

    assignee: "User" = Relationship(back_populates="assigned_tasks")
    project: "Project" = Relationship(back_populates="tasks")
