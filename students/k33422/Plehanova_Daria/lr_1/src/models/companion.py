from enum import Enum

from sqlmodel import SQLModel, Field


class Status(str, Enum):
    approved = 'approved'
    rejected = 'rejected'
    pending = "pending"


class CompanionBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')
    status: Status = Field(default=Status.pending)


class Companion(CompanionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
