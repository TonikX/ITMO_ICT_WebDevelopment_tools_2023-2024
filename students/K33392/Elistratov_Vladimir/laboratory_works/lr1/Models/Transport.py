from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from Models.Enum import TransportType


class TransportBasic(SQLModel):
    seats: int = Field()
    govNumber: str


class TransportDefault(TransportBasic):
    type: str = Field(default=TransportType.other)
    owner_id: int = Field(default=None, foreign_key="user.id")


class Transport(TransportDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    _owner: Optional["User"] = Relationship(back_populates="_transports")
    _travels: Optional[List["Travel"]] = Relationship(back_populates="_transport")
