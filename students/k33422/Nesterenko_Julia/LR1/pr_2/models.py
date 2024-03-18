from datetime import datetime
from enum import Enum
from typing import Optional, List, Union
from sqlmodel import SQLModel, Field, Relationship


class GenderType(Enum):
    undefined = "-"
    female = "f"
    male = "m"

class StatusType(Enum):
    open = "open"
    closed = "closed"
    cancelled = "cancelled"

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

class AccomodationType(Enum):
    hotel = "hotel"
    hostel = "hostel"
    apartments = "apartments"
    couchsurfing = "couchsurfing"
    tent = "tent"


class UserTripLink(SQLModel, table=True):
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id", primary_key=True)
    trip_id: Optional[int] = Field(
        default=None, foreign_key="trip.id", primary_key=True)


class UserDefault(SQLModel):
    first_name: str
    last_name: str
    gender: GenderType = "-"
    age: int
    telephone: str
    email: str
    bio: Optional[str] = ""


class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    trips: Optional[List["Trip"]] = Relationship(back_populates="members", link_model=UserTripLink)


class TripDefault(SQLModel):
    status: StatusType = "open"
    member_capacity: Optional[int] = None
    

class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    members: Optional[List["User"]] = Relationship(back_populates="trips", link_model=UserTripLink)
    steps: Optional[List["Step"]] = Relationship(back_populates="trip", 
                                                 sa_relationship_kwargs={"cascade": "all, delete"})

class TripDetailed(TripDefault):
    members: Optional[List["User"]] = None
    steps: Optional[List["Step"]] = None


class StepDefault(SQLModel):
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id")
    date_from: datetime
    date_to: datetime
    est_price: float
    stay_id: Optional[int] = Field(default=None, foreign_key="stay.id")
    #OR
    transition_id: Optional[int] = Field(default=None, foreign_key="transition.id")


class Step(StepDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    trip: Trip = Relationship(back_populates="steps")
    stay: Optional["Stay"] = Relationship(back_populates="steps")
    transition: Optional["Transition"] = Relationship(back_populates="steps")


class StepDetailed(StepDefault):
    trip: Trip = None
    stay: Optional["Stay"] = None
    transition: Optional["Transition"] = None


class TransitionDefault(SQLModel):
    location_from: str
    location_to: str
    transport: TransportType


class Transition(TransitionDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    steps: Optional[List["Step"]] = Relationship(back_populates="transition", 
                                                 sa_relationship_kwargs={"cascade": "all, delete"})


class StayDefault(SQLModel):
    location: str
    address: str
    accomodation: AccomodationType


class Stay(StayDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    steps: Optional[List["Step"]] = Relationship(back_populates="stay",
                                                 sa_relationship_kwargs={"cascade": "all, delete"})


