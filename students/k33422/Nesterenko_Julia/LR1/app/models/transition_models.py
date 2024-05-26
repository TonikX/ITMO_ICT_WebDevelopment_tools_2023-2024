from enum import Enum
from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship


class TransportType(Enum):
    plane = "plane"
    train = "train"
    ship = "ship"
    ferry = "ferry"
    bus = "bus"
    car = "car"
    motorbike = "motorbike"
    bycicle = "bycicle"
    walking = "walking"
    hitchhiking = "hitchhiking"


class TransitionDefault(SQLModel):
    location_from: str
    location_to: str
    transport: TransportType


class Transition(TransitionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    steps: Optional[List["Step"]] = Relationship(back_populates="transition", 
                                                 sa_relationship_kwargs={"cascade": "all, delete"})


from .step_models import Step
Transition.model_rebuild(_types_namespace={"Step": Step})
