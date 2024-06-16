from sqlmodel import SQLModel, Field, Relationship  # type: ignore
from typing import List, Optional
from enum import Enum

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    pass_hash: str
    bio: Optional[str] = Field(default=None)
    is_admin: bool = Field(default=False)


# Book
class BookModerationStatus(Enum):
    pending = "pending"
    approved = "approved"


class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    author: str
    year: Optional[int] = Field(default=None)
    creator_id: int = Field(foreign_key="user.id", default = 1)
    moderation_status: BookModerationStatus = Field(
        default=BookModerationStatus.pending
    )

