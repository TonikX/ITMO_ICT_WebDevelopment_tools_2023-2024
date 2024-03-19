from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from Models.Links import TravelUsersLink


class UserDefault(SQLModel):
    username: str
    firstName: str
    lastName: Optional[str] = None
    middleName: Optional[str] = None
    bio: Optional[str] = None
    age: Optional[int] = None


class UserCreate(UserDefault):
    password: str


class UserPasswordDefault(UserDefault):
    hashedPassword: str


class UserPasswordUpdate(SQLModel):
    oldPassword: str
    newPassword: str


class User(UserPasswordDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    _travelsAsLeader: Optional[List["Travel"]] = Relationship(back_populates="_leader")
    _travelAsPassenger: Optional[List["Travel"]] = Relationship(back_populates="_companions", link_model=TravelUsersLink)
    _transports: Optional[List["Transport"]] = Relationship(back_populates="_owner")
