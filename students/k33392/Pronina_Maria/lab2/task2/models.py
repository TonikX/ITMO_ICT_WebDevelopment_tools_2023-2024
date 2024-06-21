import datetime
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class UserDefault(SQLModel):
    name: str
    about: Optional[str]
    preferences: Optional[str]


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)


class UserProjectDefault(SQLModel):
    user_id: int = Field(default=None, foreign_key="user.id")
    name: str
    description: Optional[str]


class UserProject(UserProjectDefault, table=True):
    id: int = Field(default=None, primary_key=True)
