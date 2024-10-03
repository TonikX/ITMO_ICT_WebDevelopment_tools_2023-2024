from typing import TYPE_CHECKING, Optional, List
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .task import Task

# Приоритет
class PriorityDefault(SQLModel):
    name: str


class Priority(PriorityDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks_priority: Optional[List["Task"]] = Relationship(back_populates="priority")
# Приоритет
