from datetime import date
from typing import Optional

from pydantic import BaseModel
from typing_extensions import List

from model.schemas.trip_participant import TripParticipantRead
from model.schemas.user import UserRead


class TripBase(BaseModel):
    title: str
    description: Optional[str] = None
    departure_location: str
    destination: str
    start_date: date
    end_date: date
    budget: Optional[float] = None
    transport_type: Optional[str] = None
    max_participants: Optional[int] = None
    status: Optional[str] = "active"


class TripCreate(TripBase):
    pass


class TripUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    departure_location: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    transport_type: Optional[str] = None
    max_participants: Optional[int] = None
    status: Optional[str] = None


class TripRead(TripBase):
    id: int
    creator_id: int
    creator: Optional[UserRead] = None
    participants: List[TripParticipantRead] = None
