from typing import Optional
from sqlalchemy import Integer, Column, ForeignKey
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class UserTripLinkDefault(SQLModel):
    __table_args__ = (
        UniqueConstraint("trip_id", "user_id", name="unique pair of ids"),
    )
    user_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("user.id", ondelete='CASCADE'), default=None))
    trip_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("trip.id", ondelete='CASCADE'), default=None))
    role: Optional[str]

"""
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id") 
    
    user_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("user.id", onupdate="CASCADE", ondelete='CASCADE'), default=None, primary_key=True))
    trip_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("trip.id", onupdate="CASCADE", ondelete='CASCADE'), default=None, primary_key=True))
"""

class UserTripLink(UserTripLinkDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="trips")
    trip: "Trip" = Relationship(back_populates="members")


class UserTripLinkTrips(SQLModel):
    role: Optional[str]
    trip: "TripDetailed" = None


class UserTripLinkUsers(SQLModel):
    role: Optional[str]
    user: "UserDefault" = None


from models.user_models import User, UserDefault
from models.trip_models import Trip, TripDetailed
UserTripLink.model_rebuild(_types_namespace={"User": User, "Trip": Trip})
UserTripLinkTrips.model_rebuild(_types_namespace={"TripDetailed": TripDetailed})
UserTripLinkUsers.model_rebuild(_types_namespace={"UserDefault": UserDefault})