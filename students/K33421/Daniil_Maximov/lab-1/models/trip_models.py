from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional, List

class StatusType(Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class TripDefault(SQLModel):
    status: StatusType = StatusType.open
    member_amount: Optional[int] = Field(default=None, ge=0)


class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    members: Optional[List["UserTripLink"]] = Relationship(back_populates="trip",
                                                           sa_relationship_kwargs={"cascade": "all, delete"})

    # steps: Optional[List["Step"]] = Relationship(back_populates="trip",
    #                                              sa_relationship_kwargs={"cascade": "all, delete"})

from models.user_trip_link_models import UserTripLink
Trip.model_rebuild(_types_namespace={"UserTripLink": UserTripLink})