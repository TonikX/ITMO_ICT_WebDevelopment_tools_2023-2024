from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from .task import Task

if TYPE_CHECKING:
    from .user import User


# Проект
class ProjectDefault(SQLModel):
    title: str
    description: str
    user_id: int = Field(default=None, foreign_key="user.id")


class Project(ProjectDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    project_tasks: Optional[List["Task"]] = Relationship(back_populates="project")
    user: Optional["User"] = Relationship(back_populates="projects")


class ProjectOut(ProjectDefault):
    id: int
    project_tasks: Optional[List[Task]] = None
# Проект
