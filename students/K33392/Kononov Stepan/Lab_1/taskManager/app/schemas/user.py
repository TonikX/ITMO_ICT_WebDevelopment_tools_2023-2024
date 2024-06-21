from datetime import datetime
from typing import List, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from .task import Task


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    tasks: List['Task'] = []

    class Config:
        from_attributes = True
