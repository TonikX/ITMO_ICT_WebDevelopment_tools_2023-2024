from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from typing_extensions import TypedDict

from auth import AuthHandler
from connection import get_session
from models.trip_models import Trip, TripDefault
from models.user_trip_link_models import UserTripLinkDefault, UserTripLink

trip_router = APIRouter(tags=['Trips'])
auth_handler = AuthHandler()


@trip_router.get("/trip/all")
def trip_list(session: Session = Depends(get_session)) -> Sequence[Trip]:
    return session.exec(select(Trip)).all()


@trip_router.get("/trip/{trip_id}")
def trip_one(trip_id: int, session=Depends(get_session)) -> Trip:
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@trip_router.post("/trip")
def trip_create(trip: TripDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                      "data": Trip}):
    trip = Trip.model_validate(trip)
    session.add(trip)
    session.commit()
    session.refresh(trip)
    link = UserTripLinkDefault(user_id=current.id, trip_id=trip.id, role='creator')
    link = UserTripLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": trip}