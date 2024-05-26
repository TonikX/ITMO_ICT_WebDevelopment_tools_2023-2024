from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from .companion import Companion
from .favorite_trip import FavoriuteTrip
from .user import UserBaseId


class TripBase(SQLModel):
    start_location: str
    end_location: str
    start_date: datetime
    end_date: datetime
    description: str | None


class TripBasePartial(SQLModel):
    start_location: str | None = None
    end_location: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    description: str | None = None


class Trip(TripBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
    user: 'User' = Relationship(
        back_populates='created_trips'
    )
    liked_by: list['User'] = Relationship(
        back_populates='favorite_trips',
        link_model=FavoriuteTrip
    )
    companions: list['User'] = Relationship(
        back_populates='trip_requests',
        link_model=Companion,
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class TripDetail(TripBase):
    id: int | None
    liked_by: list[UserBaseId] = []
