from typing import Sequence, List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session
from typing_extensions import TypedDict

from auth import AuthHandler
from connection import get_session
from exceptions.forbbiden_exception import ForbiddenException
from exceptions.user_not_found_exception import UserNotFoundException
from models.trip_models import Trip, TripDefault, TripInput
from models.user_models import User
from models.user_trip_link_models import TripDetailed, UserTripLink, UserTripLinkDefault, UserTripLinkTrips

trip_router = APIRouter(tags=['Trips'])
auth_handler = AuthHandler()


def user_in_members(trip_id: int, user_id: int) -> bool:
    generator = get_session()
    session = next(generator)
    user = session.get(User, user_id)
    if not user:
        raise UserNotFoundException
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return user.id in [mem.user.id for mem in trip.members]


@trip_router.get("/trip/all", response_model=List[TripDetailed])
def trip_list(session: Session = Depends(get_session)) -> Sequence[Trip]:
    return session.exec(select(Trip)).all()


@trip_router.get("/trip/my")
def trip_my(session=Depends(get_session),
            current=Depends(auth_handler.current_user)) -> List[UserTripLinkTrips]:
    user = session.get(User, current.id)

    if not user:
        raise UserNotFoundException
    roles = [link.role for link in user.trips]
    trips = [TripDetailed.model_validate(link.trip) for link in user.trips]
    users_trips = [UserTripLinkTrips(role=r, trip=t) for r, t in zip(roles, trips)]
    if not user:
        raise HTTPException(status_code=404, detail="User has no trips")
    return users_trips

@trip_router.get("/trip/{trip_id}")
def trip_one(trip_id: int, session=Depends(get_session)) -> Trip:
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@trip_router.post("/trip/create")
def trip_create(trip: TripInput, session=Depends(get_session),
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
    session.refresh(trip)
    return {"status": 200, "data": trip}


@trip_router.delete("/trip/delete/{trip_id}")
def trip_delete(trip_id: int, session=Depends(get_session),
                current=Depends(auth_handler.current_user)):
    if not (current.is_admin or user_in_members(trip_id, current.id)):
        raise ForbiddenException
    trip = session.get(Trip, trip_id)
    session.delete(trip)
    session.commit()
    return {"status": 201, "message": f"deleted trip with id {trip_id}"}
