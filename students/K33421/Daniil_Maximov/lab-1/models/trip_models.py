from enum import Enum

from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional, List


class StatusType(Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class TripInput(SQLModel):
    status: str = "open"
    member_limit: Optional[int]
    location_id: Optional[int]
    transport_id: Optional[int]


class TripDefault(SQLModel):
    status: StatusType = StatusType.open
    member_limit: Optional[int] = Field(default=2, ge=0)


class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    members: Optional[List["UserTripLink"]] = Relationship(back_populates="trip",
                                                           sa_relationship_kwargs={"cascade": "all, delete"})

    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="trips")

    transport_id: Optional[int] = Field(default=None, foreign_key="transport.id")
    transport: Optional["Transport"] = Relationship(back_populates="trips")


class TripPublic(TripDefault):
    members: Optional[List["UserTripLinkUsers"]] = None
    transport: Optional["Transport"] = None
    location: Optional["Location"] = None


from models.user_trip_link_models import UserTripLink, UserTripLinkUsers
from models.location_model import Location
from models.transport_model import Transport
