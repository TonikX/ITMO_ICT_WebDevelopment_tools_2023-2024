from typing import Optional
from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
from enum import Enum
from .config import DB_URL, DB_URL_ASYNC
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    pass_hash: str
    bio: Optional[str] = Field(default=None)
    is_admin: bool = Field(default=False)


class BookModerationStatus(Enum):
    pending = "pending"
    approved = "approved"


class Book(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str = Field(unique=True)
    author: str
    year: Optional[int] = Field(default=None)
    creator_id: int = Field(foreign_key="user.id")
    moderation_status: BookModerationStatus = Field(
        default=BookModerationStatus.pending
    )


engine = create_engine(DB_URL, future=True)
engine_async = create_async_engine(DB_URL_ASYNC)
