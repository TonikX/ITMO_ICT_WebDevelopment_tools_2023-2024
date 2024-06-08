from enum import Enum

from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional, List

from models.location_model import Location


class StatusType(Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"


class TripDefault(SQLModel):
    status: StatusType = StatusType.open
    member_limit: Optional[int] = Field(default=2, ge=0)


class TripInput(SQLModel):
    status: str = "open"
    member_limit: Optional[int]


class TripDetailed(TripDefault):
    members: Optional[List["UserTripLinkUsers"]] = None
    # transportType: Optional[str] = None
    location: Optional[List[Location]] = None
#    todo доделать тут
# помнить про ковычки
# сделать методы для добавления локации и транспорта


class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    members: Optional[List["UserTripLink"]] = Relationship(back_populates="trip",
                                                           sa_relationship_kwargs={"cascade": "all, delete"})


from models.user_trip_link_models import UserTripLink, UserTripLinkUsers
