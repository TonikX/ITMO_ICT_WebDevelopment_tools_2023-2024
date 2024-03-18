from datetime import datetime
from enum import Enum
from typing import Optional, List, Union

from pydantic import BaseModel


class GenderType(Enum):
    female = "f"
    male = "m"
    undefined = "-"

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


class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    gender: GenderType
    age: int
    telephone: str
    email: str
    bio: str
    

class Transition(BaseModel):
    id: int
    location_from: str
    location_to: str
    transport: TransportType


class Stay(BaseModel):
    id: int
    location: str
    address: str
    accomodation: AccomodationType


class Step(BaseModel):
    id: int
    date_from: datetime
    date_to: datetime
    est_price: int
    contents: Union[Transition, Stay]


class Trip(BaseModel):
    id: int
    status: StatusType
    member_capacity: Optional[int] = None
    members: List[User]
    steps: Optional[List[Step]] = []