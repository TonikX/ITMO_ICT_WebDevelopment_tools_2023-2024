from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional, List


class StatusType(Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class TripInput(SQLModel):
    status: str = "open"
    location_id: Optional[int]


class TripDefault(SQLModel):
    status: StatusType = StatusType.open
    member_limit: Optional[int] = Field(default=2, ge=0)


class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    members: Optional[List["UserTripLink"]] = Relationship(back_populates="trip")

    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="trips")

    steps: Optional[List["Step"]] = Relationship(back_populates="trip")


class TripDetailed(TripDefault):
    id: Optional[int]
    members: Optional[List["UserTripLinkUsers"]] = None
    location: Optional["Location"] = None
    steps: Optional[List["Step"]] = None


from models.user_trip_link_models import UserTripLink, UserTripLinkUsers
from models.location_models import Location
from models.step_models import Step
