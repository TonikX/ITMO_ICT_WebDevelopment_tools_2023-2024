from datetime import datetime

from sqlmodel import SQLModel, Field, Relationship

from .favorite_trip import FavoriuteTrip


class TripBase(SQLModel):
    start_location: str
    end_location: str
    start_date: datetime
    end_date: datetime
    description: str | None


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
