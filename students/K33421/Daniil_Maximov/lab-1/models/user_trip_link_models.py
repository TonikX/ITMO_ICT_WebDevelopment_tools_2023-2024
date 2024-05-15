from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship, UniqueConstraint


class UserTripLinkDefault(SQLModel):
    user_id: Optional[int] = Field(sa_column=Column(Integer,
                                                    ForeignKey("user.id", ondelete='CASCADE'), default=None))

    trip_id: Optional[int] = Field(sa_column=Column(Integer,
                                                    ForeignKey("trip.id", ondelete='CASCADE'), default=None))

    role: Optional[str]


class UserTripLink(UserTripLinkDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    user: "User" = Relationship(back_populates="trips")
    trip: "Trip" = Relationship(back_populates="members")


from models.user_models import User
from models.trip_models import Trip
UserTripLink.model_rebuild(_types_namespace={"User": User, "Trip": Trip})
# UserTripLinkTrips.model_rebuild(_types_namespace={"TripDetailed": TripDetailed})
# UserTripLinkUsers.model_rebuild(_types_namespace={"UserDefault": UserDefault})
