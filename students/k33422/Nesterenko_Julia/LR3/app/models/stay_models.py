from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class AccomodationType(Enum):
    hotel = "hotel"
    hostel = "hostel"
    apartments = "apartments"
    couchsurfing = "couchsurfing"
    tent = "tent"


class StayDefault(SQLModel):
    location: str
    address: str
    accomodation: AccomodationType


class Stay(StayDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    steps: Optional[List["Step"]] = Relationship(back_populates="stay",
                                                 sa_relationship_kwargs={"cascade": "all, delete"})
    

from .step_models import Step
Stay.model_rebuild(_types_namespace={"Step": Step})