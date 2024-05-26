from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select

from app.models.user_models import * 
from app.models.trip_models import * 
from app.models.usertriplink_models import *
from app.connection import *
from app.auth import AuthHandler


trip_router = APIRouter()
auth_handler = AuthHandler()


def user_in_members(trip_id: int, user_id: int) -> bool:
    generator = get_session()
    session = next(generator)
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return user.id in [mem.user.id for mem in trip.members]


# all trips
@trip_router.get("/trip/all", response_model=List[TripDetailed], tags=['Trips'])
def trip_list(session=Depends(get_session)) -> List[Trip]:
    return session.exec(select(Trip)).all()


# current user's trips
@trip_router.get("/trip/my", tags=['Trips'])
def trip_my(session=Depends(get_session), 
            current=Depends(auth_handler.current_user)) -> List[UserTripLinkTrips]:
    user = session.get(User, current.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles = [link.role for link in user.trips]
    trips = [TripDetailed.model_validate(link.trip) for link in user.trips]
    users_trips = [UserTripLinkTrips(role=r, trip=t) for r, t in zip(roles, trips)]
    if not user:
        raise HTTPException(status_code=404, detail="User has no trips")
    return users_trips


# one trip
@trip_router.get("/trip/{trip_id}", response_model=TripDetailed, tags=['Trips'])
def trip_one(trip_id: int, session=Depends(get_session)) -> Trip:
    #return session.exec(select(Trip).where(Trip.id == trip_id)).first()
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


# add trip
@trip_router.post("/trip", tags=['Trips'])
def trip_create(trip: TripDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                      "data": Trip}):
    trip = Trip.model_validate(trip)
    session.add(trip)
    session.commit()
    session.refresh(trip)
    link = UserTripLinkDefault(user_id = current.id, trip_id = trip.id, role = 'creator')
    link = UserTripLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": trip}


# delete trip
@trip_router.delete("/trip/delete/{trip_id}", tags=['Trips'])
def trip_delete(trip_id: int, session=Depends(get_session),
                current=Depends(auth_handler.current_user)):
    if not (current.is_admin or user_in_members(trip_id, current.id)):
        raise HTTPException(status_code=403, detail="You have no access to this trip")
    trip = session.get(Trip, trip_id)
    session.delete(trip)
    session.commit()
    return {"status": 201, "message": f"deleted trip with id {trip_id}"}


# update trip
@trip_router.patch("/trip/edit/{trip_id}", response_model=TripDetailed, tags=['Trips'])
def trip_update(trip_id: int, trip: TripDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> Trip:
    if not (current.is_admin or user_in_members(trip_id, current.id)):
        raise HTTPException(status_code=403, detail="You have no access to this trip")
    db_trip = session.get(Trip, trip_id)
    trip_data = trip.model_dump(exclude_unset=True)
    for key, value in trip_data.items():
        setattr(db_trip, key, value)
    session.add(db_trip)
    session.commit()
    session.refresh(db_trip)
    return db_trip