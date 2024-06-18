from typing import List

from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional
from models.trip_models import Trip


class LocationDefault(SQLModel):
    name: str
    description: str
    country: str


class Location(LocationDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    trips: Optional[List["Trip"]] = Relationship(back_populates="location")
