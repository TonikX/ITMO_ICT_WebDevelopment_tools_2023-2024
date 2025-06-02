from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from db.connection import get_session
from model.models.models import Trip, User, TripParticipant
from model.schemas.trip import TripCreate, TripRead, TripUpdate
from auth.auth import AuthHandler
from model.schemas.trip_participant import TripParticipantCreate, TripParticipantRead, TripParticipantUpdate

trip_router = APIRouter()
auth_handler = AuthHandler()


@trip_router.post("/", response_model=TripRead)
def create_trip(
    trip: TripCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(auth_handler.get_current_user)
):
    db_trip = Trip(**trip.model_dump(), creator_id=current_user.id)
    session.add(db_trip)
    session.commit()
    session.refresh(db_trip)
    return db_trip


@trip_router.get("/", response_model=List[TripRead])
def get_trips(session: Session = Depends(get_session)):
    return session.exec(select(Trip)).all()


@trip_router.get("/{trip_id}", response_model=TripRead)
def get_trip(trip_id: int, session: Session = Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@trip_router.patch("/{trip_id}", response_model=TripRead)
def update_trip(trip_id: int, update: TripUpdate, session: Session = Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(trip, key, value)
    session.commit()
    session.refresh(trip)
    return trip


@trip_router.delete("/{trip_id}", response_model=dict)
def delete_trip(trip_id: int, session: Session = Depends(get_session)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    session.delete(trip)
    session.commit()
    return {"ok": True}


@trip_router.post("/{trip_id}/participants", response_model=TripParticipantRead)
def create_trip_participant(trip_id: int, data: TripParticipantCreate, session: Session = Depends(get_session)):
    participant = TripParticipant(
        trip_id=trip_id,
        user_id=data.user_id,
        message=data.message
    )
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return participant


@trip_router.get("/{trip_id}/", response_model=List[TripParticipantRead])
def get_all_participants(trip_id: int, session: Session = Depends(get_session)):
    return session.exec(select(TripParticipant).where(TripParticipant.trip_id == trip_id)).all()


@trip_router.get("/{trip_id}/participants/{user_id}", response_model=TripParticipantRead)
def get_trip_participant(trip_id: int, user_id: int, session: Session = Depends(get_session)):
    participant = session.get(TripParticipant, (trip_id, user_id))
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


@trip_router.patch("/{trip_id}/participants/{user_id}", response_model=TripParticipantRead)
def update_trip_participant(trip_id: int, user_id: int, update: TripParticipantUpdate, session: Session = Depends(get_session)):
    participant = session.get(TripParticipant, (trip_id, user_id))
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    update_data = update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(participant, key, value)
    session.commit()
    session.refresh(participant)
    return participant


@trip_router.delete("/{trip_id}/participants/{user_id}", response_model=dict)
def delete_trip_participant(trip_id: int, user_id: int, session: Session = Depends(get_session)):
    participant = session.get(TripParticipant, (trip_id, user_id))
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    session.delete(participant)
    session.commit()
    return {"ok": True}