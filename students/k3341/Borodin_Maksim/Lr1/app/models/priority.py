from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.task import Task


class Priority(SQLModel, table=True):
    __tablename__ = "priorities"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True, max_length=50)
    weight: int = Field(default=1, ge=1, le=10)
    description: str | None = Field(default=None, max_length=255)

    tasks: list["Task"] = Relationship(back_populates="priority")
