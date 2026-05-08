from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.notification import Notification
    from app.models.schedule import Schedule
    from app.models.task import Task


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, max_length=255)
    username: str = Field(index=True, unique=True, max_length=100)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    tasks: list["Task"] = Relationship(back_populates="user")
    schedules: list["Schedule"] = Relationship(back_populates="user")
    notifications: list["Notification"] = Relationship(back_populates="user")
