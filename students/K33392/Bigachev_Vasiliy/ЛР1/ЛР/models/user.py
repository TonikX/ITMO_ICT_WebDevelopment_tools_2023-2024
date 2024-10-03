from typing import TYPE_CHECKING, Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

from .project import Project


class UserDefault(SQLModel):
    nickname: str
    email: str
    hashed_password: str
    createdAt: None | date = date.today()


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    projects: Optional[List[Project]] = Relationship(back_populates="user")


class UserOut(UserDefault):
    id: int
    projects: Optional[List[Project]] = None


class UserSignIn(SQLModel):
    nickname: str
    password: str


class UserSignUp(SQLModel):
    nickname: str
    email: str
    password: str
