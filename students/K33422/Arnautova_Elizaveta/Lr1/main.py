from __future__ import annotations

from datetime import date
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import service
import models
import dtos
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/users/', response_model=dtos.UserOutFull)
def create_user(user: dtos.UserCreate, db: Session = Depends(get_db)):
    db_user = service.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail='Username already registered')
    new_user = service.create_user(db=db, user=user)
    return service.get_user_full(db, new_user)


@app.put('/users/{user_id}', response_model=dtos.UserOutFull)
def update_user(user_id: int, user: dtos.UserInfo, db: Session = Depends(get_db)):
    user_upd = service.update_user(db, user_id, user)
    return service.get_user_full(db, user_upd)


@app.get('/users/', response_model=list[dtos.UserOutBrief])
def read_users(db: Session = Depends(get_db)):
    users = service.get_users(db)
    return users


@app.get('/users/{user_id}', response_model=dtos.UserOutFull)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return service.get_user_full(db, db_user)


@app.post('/users/{user_id}/trip/', response_model=dtos.TripPlanned)
def create_trip_for_user(user_id: int, trip: dtos.TripCreate, db: Session = Depends(get_db)):
    return service.create_user_trip(db, trip, user_id)


@app.get('/trips/', response_model=list[dtos.TripPlanned])
def read_trips(db: Session = Depends(get_db)):
    return service.get_trips(db)


@app.get('/matches/{user_id}', response_model=list[dtos.UserOutBrief])
def get_matches(user_id: int, db: Session = Depends(get_db)):
    return service.get_users_by_ids(db, service.get_match_list(db, user_id))


@app.post('/swipe/{user_id}')
def swipe(user_id: int, recipient_id: int, is_right: bool, db: Session = Depends(get_db)):
    if service.check_swipe(db, user_id, recipient_id):
        raise HTTPException(status_code=400, detail='Swipe for this user already exists')
    service.swipe(db, user_id, recipient_id, is_right)
    return {'result': 'ok'}


@app.post('/trip/{user_id}/request_join/')
def request_join(user_id: int, trip_id: int, db: Session = Depends(get_db)):
    if trip_id in list(map(lambda request: request.id, service.get_user_requests(db, user_id))):
        raise HTTPException(status_code=400, detail="You've already sent request for this trip")
    if service.get_trip(db, trip_id).initiator_id not in service.get_match_list(db, user_id):
        raise HTTPException(status_code=400, detail="You can't join this trip. It's illegal. "
                                                    "Wherever you even got this id anyway?")
    service.request_trip_join(db, user_id, trip_id)
    return {'result': 'ok'}


@app.post('/trip/{user_id}/process_request/')
def process_request(user_id: int, request_id: int, accept: bool, db: Session = Depends(get_db)):
    request = service.get_request(db, request_id)
    if request.trip.initiator_id != user_id:
        raise HTTPException(status_code=400, detail="This isn't your request, put it down on the ground slowly")
    if request.accepted is not None:
        raise HTTPException(status_code=400, detail="This request is already processed")
    service.process_join_request(db, request_id, accept)
    return {'result': 'ok'}


@app.get('/search/{user_id}', response_model=dtos.UserOutFull)
def search(user_id: int, region_id: int | None = None, place_id: int | None = None,
           departure_before: date | None = None, departure_after: date | None = None,
           return_before: date | None = None, return_after: date | None = None, db: Session = Depends(get_db)):
    if place_id and service.get_place(db, place_id).region_id != region_id:
        raise HTTPException(status_code=400, detail='Learn your geography mate, your destination is in another region')
    departure_sanity_check = departure_after and departure_before and departure_after > departure_before
    return_sanity_check = return_after and return_before and return_after > return_before
    intersect_sanity_check = return_before and departure_after and departure_after > return_before
    if departure_sanity_check or return_sanity_check or intersect_sanity_check:
        raise HTTPException(status_code=400, detail="Congratulations, you broke time. Don't do it again. Please.")
    companion = service.find_companion(db, user_id, region_id, place_id, departure_before,
                                       departure_after, return_before, return_after)
    if companion:
        return companion
    else:
        raise HTTPException(status_code=400, detail="Sorry, we couldn't find you a companion with these parameters.")
