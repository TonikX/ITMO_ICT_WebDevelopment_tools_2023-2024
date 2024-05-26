from datetime import datetime
from typing import Optional
from pydantic import validator
from sqlalchemy import Integer, Column, ForeignKey
from sqlmodel import SQLModel, Field, Relationship


class StepDefault(SQLModel):
    #trip_id: Optional[int] = Field(default=None, foreign_key="trip.id")
    trip_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("trip.id", ondelete='CASCADE'), default=None))
    date_from: datetime = Field()
    date_to: datetime = Field()
    est_price: float = Field(default=0, ge=0)
    #stay_id: Optional[int] = Field(default=None, foreign_key="stay.id")
    stay_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("stay.id", ondelete='CASCADE'), default=None))
    #OR
    #transition_id: Optional[int] = Field(default=None, foreign_key="transition.id")
    transition_id: Optional[int] = Field(sa_column=Column(Integer,
        ForeignKey("transition.id", ondelete='CASCADE'), default=None))

    @validator('date_to')
    def from_lt_to(cls, date, values, **kwargs):
            if 'date_from' in values and date < values['date_from']:
                raise ValueError("date_to should be later than date_from")
            return date
    

class Step(StepDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    trip: "Trip" = Relationship(back_populates="steps")
    stay: Optional["Stay"] = Relationship(back_populates="steps")
    transition: Optional["Transition"] = Relationship(back_populates="steps")


class StepDetailed(StepDefault):
    trip: "Trip" = None
    stay: Optional["Stay"] = None
    transition: Optional["Transition"] = None


from .trip_models import Trip
from .stay_models import Stay
from .transition_models import Transition
Step.model_rebuild(_types_namespace={"Trip": Trip, "Stay": Stay, "Transition": Transition})
StepDetailed.model_rebuild(_types_namespace={"Trip": Trip, "Stay": Stay, "Transition": Transition})
