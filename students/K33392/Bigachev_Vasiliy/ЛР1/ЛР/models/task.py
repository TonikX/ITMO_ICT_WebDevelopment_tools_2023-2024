from typing import TYPE_CHECKING, Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

from .tag import TagTaskLink
from .priority import Priority
from .tag import Tag

if TYPE_CHECKING:
    from .project import Project


# Задача
class TaskDefault(SQLModel):
    title: str
    description: str
    dueTo: date
    createdAt: None | date = date.today()
    priority_id: Optional[int] = Field(default=None, foreign_key="priority.id")
    project_id: Optional[int] = Field(default=None, foreign_key="project.id")


class Task(TaskDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    priority: Optional["Priority"] = Relationship(back_populates="tasks_priority")
    tags: Optional[List["Tag"]] | None = Relationship(back_populates="tasks", link_model=TagTaskLink)
    project: Optional["Project"] = Relationship(back_populates="project_tasks")


class TaskOut(TaskDefault):
    id: int
    priority: Optional[Priority] = None
    tags: Optional[List[Tag]] = None
# Задача