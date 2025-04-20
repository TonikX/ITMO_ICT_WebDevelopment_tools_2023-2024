from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from model.models.models import ParticipationStatus


class TripParticipantBase(BaseModel):
    status: Optional[ParticipationStatus] = ParticipationStatus.pending
    message: Optional[str] = None


class TripParticipantCreate(BaseModel):
    user_id: int
    message: Optional[str] = None


class TripParticipantUpdate(BaseModel):
    status: Optional[ParticipationStatus] = None
    message: Optional[str] = None


class TripParticipantRead(BaseModel):
    trip_id: int
    user_id: int
    status: ParticipationStatus
    message: Optional[str] = None
    joined_at: datetime