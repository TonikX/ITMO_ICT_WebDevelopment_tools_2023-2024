from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint



class Role(Enum):
    owner = "owner"
    member = "member"


class UserTripLinkDefault(SQLModel):
    user_id: Optional[int] = Field(sa_column=Column(Integer,
                                                    ForeignKey("user.id", ondelete='CASCADE'), default=None))

    trip_id: Optional[int] = Field(sa_column=Column(Integer,
                                                    ForeignKey("trip.id", ondelete='CASCADE'), default=None))

    role: Optional[str] = Field(Role.member)


class UserTripLink(UserTripLinkDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="trips")
    trip: "Trip" = Relationship(back_populates="members")

class UserTripLinkUsers(SQLModel):
    role: Optional[str]
    user: "UserDefault" = None


class UserTripLinkTrips(SQLModel):
    role: Optional[str]
    trip: "TripPublic" = None


from models.user_models import User, UserDefault
from models.trip_models import Trip, TripPublic