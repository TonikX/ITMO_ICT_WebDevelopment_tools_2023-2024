from sqlmodel import SQLModel, Field


class FavoriuteTripBase(SQLModel):
    trip_id: int = Field(foreign_key='trip.id')


class FavoriuteTrip(FavoriuteTripBase, table=True):
    __tablename__ = 'favorite_trip'

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='user.id')
