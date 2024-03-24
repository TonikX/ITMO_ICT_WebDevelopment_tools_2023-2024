from datetime import date
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

from .favorite_trip import FavoriuteTrip


class Gender(str, Enum):
    male = "male"
    female = "female"


class UserBase(SQLModel):
    email: str = Field(unique=True)
    first_name: str
    last_name: str
    gender: Gender
    birth_date: date
    description: str | None
    county: str
    language: str


class UserPasswordUpdate(SQLModel):
    old_password: str
    new_password: str


class UserPasswordCreate(UserBase):
    password: str


class UserPassword(UserBase):
    password_hash: bytes


class User(UserPassword, table=True):
    id: int | None = Field(default=None, primary_key=True)
    favorite_trips: list['Trip'] = Relationship(
        back_populates='liked_by',
        sa_relationship_kwargs={"cascade": "all, delete"},
        link_model=FavoriuteTrip
    )
    reviews: list['Review'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
    created_trips: list['Trip'] = Relationship(
        back_populates='user',
        sa_relationship_kwargs={"cascade": "all, delete"},
    )
