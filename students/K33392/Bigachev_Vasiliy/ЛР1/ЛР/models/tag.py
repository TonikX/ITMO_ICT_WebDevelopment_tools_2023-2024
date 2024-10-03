from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .task import Task


# Тэг
class TagTaskLink(SQLModel, table=True):
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    task_id: Optional[int] = Field(default=None, foreign_key="task.id", primary_key=True)


class TagDefault(SQLModel):
    name: str


class Tag(TagDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    tasks: Optional[List["Task"]] = Relationship(back_populates="tags", link_model=TagTaskLink)
# Тэг
