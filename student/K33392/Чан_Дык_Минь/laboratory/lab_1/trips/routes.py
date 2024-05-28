from connection import init_db, get_session
from fastapi import FastAPI, Depends, HTTPException, APIRouter, Query
from sqlmodel import select 
from models import *
from typing_extensions import TypedDict
from auth.auth import AuthHandler

router = APIRouter()
auth_handler = AuthHandler()

# Trips endpoints
@router.get('/trip', tags=["trips"])
def trip_get(
    departure: str = Query(None),
    destination: str = Query(None),
    date_start: date = Query(None),
    date_end: date = Query(None),
    session=Depends(get_session)
) -> List[TripUsers]:
    query = session.query(Trip)
    
    if departure:
        query = query.filter(Trip.departure == departure)
    if destination:
        query = query.filter(Trip.destination == destination)
    if date_start:
        query = query.filter(Trip.date_start == date_start)
    if date_end:
        query = query.filter(Trip.date_end == date_end)

    trips = query.all()

    if not trips:
        raise HTTPException(status_code=404, detail="No trips found with the specified criteria")
    
    # Retrieve associated users for each trip
    trip_users = []
    for trip in trips:
        # Fetch TripUserLink instances associated with the trip
        trip_user_links = session.query(TripUserLink).filter(TripUserLink.trip_id == trip.id).all()
        users = []
        # For each TripUserLink, fetch the corresponding User
        for link in trip_user_links:
            user = session.query(User).filter(User.id == link.user_id).first()
            if user:
                users.append(user.username)
        trip_users.append(TripUsers(trip=trip, users=users))

    return trip_users


@router.post('/trip', tags=["trips"])
def trip_create(trip: TripDefault, session=Depends(get_session), 
                current_user: User = Depends(auth_handler.get_current_user)) -> TypedDict('Response', {"status": int, "data": Trip}): # type: ignore
    trip = Trip.model_validate(trip)
    session.add(trip)
    session.commit()
    session.refresh(trip)
    return {"status": 200, "data": trip}

@router.delete('/trip/delete{trip_id}', tags=["trips"])
def trip_delete(trip_id: int, session=Depends(get_session), current_user: User = Depends(auth_handler.get_current_user)):
    trip = session.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    session.delete(trip)
    session.commit()
    return {"ok": True}

@router.patch('/trip/{trip_id}', tags=["trips"])
def trip_update(trip_id: int, trip: TripDefault, 
                current_user: User = Depends(auth_handler.get_current_user), 
                session=Depends(get_session)) -> TripDefault:
    db_trip = session.get(Trip, trip_id)
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    trip_data = trip.model_dump(exclude_unset=True)
    for key, value in trip_data.items():
        setattr(db_trip, key, value)
    session.add(db_trip)
    session.commit()
    session.refresh(db_trip)
    return db_trip


@router.get('/trip/{trip_id}/trip-requests', tags=["user trip request"])
def trip_requests_get(trip_id: int, 
                      session=Depends(get_session), 
                      current_user: User = Depends(auth_handler.get_current_user)) -> List[TripRequest]:
    trip = session.exec(select(TripRequest).filter(TripRequest.trip_id == trip_id)).all()
    if not trip:
        raise HTTPException(status_code=404, detail="trip is not found")
    return trip


@router.delete('/trip/delete{trip_id}/trip-requests', tags=["user trip request"])
def trip_requests_delete(trip_request_id: int, 
                         session=Depends(get_session), 
                         current_user: User = Depends(auth_handler.get_current_user),):
    request = session.get(TripRequest, trip_request_id)
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    session.delete(request)
    session.commit()
    return {"ok": True}

@router.post('/trip/{user_id}/trip-request', tags=["user trip request"])
def trip_request_create(user_id: int, trip_request: TripRequestDefault, 
                        current_user: User = Depends(auth_handler.get_current_user), 
                        session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": TripRequest}): # type: ignore
    trip_request_data = trip_request.dict()
    trip_request_data["user_request_id"] = user_id
    trip_request_model = TripRequest(**trip_request_data)
    
    user_request = session.exec(select(TripRequest).filter(
        (TripRequest.user_request_id == user_id) &
        (TripRequest.trip_id == trip_request_model.trip_id)
    )).first()
    
    if user_request:
        raise HTTPException(status_code=404, detail="User has already requested")
    
    session.add(trip_request_model)
    session.commit()
    session.refresh(trip_request_model)
    return {"status": 200, "data": trip_request_model}

@router.patch("/trip-request/{request_id}", tags=["user trip request"])
def update_trip_request_status(request_id: int, 
                               request_status: RequestStatus, 
                               current_user: User = Depends(auth_handler.get_current_user), 
                               session=Depends(get_session)) -> TripRequest:
    trip_request = session.get(TripRequest, request_id)
    if not trip_request:
        raise HTTPException(status_code=404, detail="Trip request not found")
    trip_request.request_status = request_status
    session.add(trip_request)
    session.commit()
    session.refresh(trip_request)
    return trip_request

# Trip User Management Endpoints
@router.post('/trip/{trip_id}/add-user/{user_id}', tags=["trip management"])
def add_user_to_trip(trip_id: int, 
                     user_id: int, 
                     session=Depends(get_session),
                     current_user: User = Depends(auth_handler.get_current_user)):
    # Check if the user is already added to the trip
    existing_link = session.exec(select(TripUserLink).filter_by(trip_id=trip_id, user_id=user_id)).first()
    if existing_link:
        return {"message": "User is already added to the trip"}
    
    trip = session.get(Trip, trip_id)
    user = session.get(User, user_id)
    if not trip or not user:
        raise HTTPException(status_code=404, detail="Trip or user not found")
    trip_user_link = TripUserLink(trip_id=trip_id, user_id=user_id)
    session.add(trip_user_link)
    session.commit()
    return {"ok": True}

@router.delete('/trip/{trip_id}/remove-user/{user_id}', tags=["trip management"])
def remove_user_from_trip(trip_id: int, 
                          user_id: int, 
                          session=Depends(get_session),
                          current_user: User = Depends(auth_handler.get_current_user)):
    # Query TripUserLink to find the entry corresponding to trip_id and user_id
    trip_user_link = session.exec(select(TripUserLink).filter_by(trip_id=trip_id, user_id=user_id)).first()
    if not trip_user_link:
        raise HTTPException(status_code=404, detail="Trip or user not found in the trip")
    
    # Delete the entry
    session.delete(trip_user_link)
    session.commit()
    return {"ok": True}