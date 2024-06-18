from sqlmodel import SQLModel, Field, Relationship
from typing_extensions import Optional
from models.trip_models import Trip


class StepDefault(SQLModel):
    name: str
    description: str
    duration: int
    trip_id: int


class Step(StepDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id")
    trip: Optional["Trip"] = Relationship(back_populates="steps")

