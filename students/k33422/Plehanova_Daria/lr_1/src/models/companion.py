from enum import Enum

from sqlmodel import SQLModel, Field

from .user import UserBaseId


class Status(str, Enum):
    approved = 'approved'
    rejected = 'rejected'
    pending = "pending"


class StatusScheme(SQLModel):
    status: Status | None = None

class CompanionBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')
    status: Status = Field(default=Status.pending)


class CompanionBaseId(CompanionBase):
    id: int


class CompanionBaseDetail(CompanionBaseId):
    user: UserBaseId


class Companion(CompanionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
