[Ссылка на практики](https://github.com/LizaArnautova/ITMO_ICT_WebDevelopment_tools_2023-2024/tree/main/students/K33422/Arnautova_Elizaveta/Lr1/practice)

Схема БД:
![](screenshots/bd.png)

Реализовано следующими классами:

**models**
```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    personal_information = Column(String)
    travelling_skills = Column(String)
    personal_transport = Column(String)
    companion_preferences = Column(String)

    owned_trips = relationship('Trip', foreign_keys='Trip.initiator_id', back_populates='initiator')


class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    initiator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    companion_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(Date)
    expected_end_date = Column(Date)
    is_completed = Column(Boolean)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    place_id = Column(Integer, ForeignKey('place.id'))

    initiator = relationship('User', foreign_keys=[initiator_id])
    companion = relationship('User', foreign_keys=[companion_id])
    region = relationship('Region', foreign_keys=[region_id])
    place = relationship('Place', foreign_keys=[place_id])
    requests = relationship('TripJoinRequest', back_populates='trip')


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    places = relationship('Place', back_populates='region')


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'))

    region = relationship('Region', back_populates='places')


class Swipe(Base):
    __tablename__ = 'swipe'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_right = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint('sender_id', 'recipient_id'),)


class TripJoinRequest(Base):
    __tablename__ = 'trip_join_request'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trip_id = Column(Integer, ForeignKey('trip.id'), nullable=False)
    accepted = Column(Boolean)

    trip = relationship('Trip', back_populates='requests')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)

```



Подключение к базе выполнено в отдельном файле, чтобы не нагружать остальные:

**database**
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:12345678@localhost:5432/tripder'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
```

Структура проекта:

![](screenshots/project.png)



**main:**

```python
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

```

**dtos:**
```python
from __future__ import annotations

from datetime import date

from pydantic import BaseModel


class TripBase(BaseModel):
    title: str
    description: str | None = None
    region_id: int
    place_id: int | None = None
    start_date: date | None = None
    expected_end_date: date | None = None


class TripCreate(TripBase):
    pass


class TripPlanned(TripBase):
    id: int
    initiator_id: int
    companion_id: int | None

    class Config:
        orm_mode = True


class TripCompleted(TripBase):
    id: int
    initiator_id: int
    companion_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    username: str


class UserInfo(UserBase):
    personal_information: str | None
    travelling_skills: str | None
    personal_transport: str | None
    companion_preferences: str | None


class UserCreate(UserInfo):
    password: str


class UserOutFull(UserInfo):
    id: int
    is_active: bool
    planned_trips: list[TripPlanned]
    completed_trips: list[TripCompleted]

    class Config:
        orm_mode = True


class UserOutBrief(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

```


**service:**
```python
from __future__ import annotations

from sqlalchemy.orm import Session
from sqlalchemy import true, false

from dtos import *
from models import *


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_full(db: Session, user: User):
    user_res = UserOutFull(
        id=user.id,
        personal_information=user.personal_information,
        travelling_skills=user.travelling_skills,
        personal_transport=user.personal_transport,
        companion_preferences=user.companion_preferences,
        username=user.username,
        is_active=user.is_active,
        planned_trips=get_user_planned_trips(db, user.id),
        completed_trips=get_user_completed_trips(db, user.id)
    )
    return user_res


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + 'muchsecure'
    db_user = User(
        username=user.username,
        hashed_password=fake_hashed_password,
        personal_information=user.personal_information,
        travelling_skills=user.travelling_skills,
        personal_transport=user.personal_transport,
        companion_preferences=user.companion_preferences
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserInfo):
    prev_user = db.query(User).filter(User.id == user_id).first()
    prev_user.username = user_update.username
    prev_user.personal_information = user_update.personal_information
    prev_user.travelling_skills = user_update.travelling_skills
    prev_user.personal_transport = user_update.personal_transport
    prev_user.companion_preferences = user_update.companion_preferences
    db.add(prev_user)
    db.commit()
    db.refresh(prev_user)
    return prev_user


def get_trips(db: Session):
    return db.query(Trip).all()


def get_trip(db: Session, trip_id: int):
    return db.query(Trip).filter(Trip.id == trip_id).first()


def get_place(db: Session, place_id: int) -> Place:
    return db.query(Place).get(place_id)


def get_joinable_trips(db: Session, user_id: int):
    matches = get_match_list(db, user_id)
    return db.query(Trip).filter(Trip.initiator_id.in_(matches) & Trip.companion_id.is_(None) & (Trip.is_completed == false()))


def create_user_trip(db: Session, trip: TripCreate, user_id: int):
    db_trip = Trip(**trip.dict(), initiator_id=user_id)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


def get_user_planned_trips(db: Session, user_id: int):
    trips = db.query(Trip).filter((Trip.initiator_id == user_id) and (Trip.is_completed == false()))
    return map(lambda trip: TripPlanned(
        id=trip.id,
        title=trip.title,
        description=trip.description,
        region_id=trip.region_id,
        place_id=trip.place_id,
        start_date=trip.start_date,
        expected_end_date=trip.expected_end_date,
        initiator_id=trip.initiator_id,
        companion_id=trip.companion_id
    ), trips)


def get_user_completed_trips(db: Session, user_id: int):
    trips = db.query(Trip).filter(((Trip.initiator_id == user_id) or (Trip.companion_id == user_id))
                                  and (Trip.is_completed == true()))
    return map(lambda trip: TripCompleted(
        id=trip.id,
        title=trip.title,
        description=trip.description,
        region_id=trip.region_id,
        place_id=trip.place_id,
        start_date=trip.start_date,
        expected_end_date=trip.expected_end_date,
        initiator_id=trip.initiator_id,
        companion_id=trip.companion_id
    ), trips)


def get_match_list(db: Session, user_id: int):
    my_swipes = db.query(Swipe).filter((Swipe.sender_id == user_id) & (Swipe.is_right == true())).all()
    res = list(filter(
        lambda swipe: db.query(Swipe).filter((Swipe.recipient_id == user_id) & (Swipe.sender_id == swipe.recipient_id)
                                             & (Swipe.is_right == true())).first(),
        my_swipes))
    return list(map(lambda swipe: swipe.recipient_id, res))


def get_white_list(db: Session, user_id: int):
    white_swipes = db.query(Swipe).filter((Swipe.recipient_id == user_id) & (Swipe.is_right == true())).all()
    return list(map(lambda swipe: swipe.sender_id, white_swipes))


def get_black_list(db: Session, user_id: int):
    black_swipes = db.query(Swipe).filter(Swipe.sender_id == user_id).all()
    return list(map(lambda swipe: swipe.recipient_id, black_swipes))


def get_users_by_ids(db: Session, user_list: list[int]):
    return db.query(User).filter(User.id.in_(user_list))


def swipe(db: Session, user_id: int, candidate_id: int, right: bool):
    db_swipe = Swipe(sender_id=user_id, recipient_id=candidate_id, is_right=right)
    db.add(db_swipe)
    db.commit()
    db.refresh(db_swipe)
    return db_swipe


def check_swipe(db: Session, user_id: int, candidate_id: int):
    return db.query(Swipe).filter((Swipe.sender_id == user_id) & (Swipe.recipient_id == candidate_id)).first()


def request_trip_join(db: Session, user_id: int, trip_id: int):
    db_request = TripJoinRequest(sender_id=user_id, trip_id=trip_id)
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request


def get_user_requests(db: Session, user_id: int):
    return db.query(TripJoinRequest).filter(TripJoinRequest.sender_id == user_id).all()


def get_request(db: Session, request_id: int) -> TripJoinRequest:
    return db.query(TripJoinRequest).get(request_id)


def process_join_request(db: Session, request_id, request_accepted: bool):
    request = db.query(TripJoinRequest).filter(TripJoinRequest.id == request_id).first()
    request.accepted = request_accepted
    db.add(request)
    if request_accepted:
        trip = request.trip
        trip.companion_id = request.sender_id
        db.add(trip)
        db.commit()
        db.refresh(request)
        db.refresh(trip)
    else:
        db.commit()
        db.refresh(request)
    return request


def find_companion(db: Session, user_id: int, region_id: int | None, place_id: int | None,
                   departure_before: date | None, departure_after: date | None,
                   return_before: date | None, return_after: date | None):
    black_list = get_black_list(db, user_id)

    filters = []
    if region_id:
        filters.append(Trip.region_id == region_id)
    if place_id:
        filters.append(Trip.place_id == place_id)
    if departure_before:
        filters.append(Trip.start_date <= departure_before)
    if departure_after:
        filters.append(Trip.start_date >= departure_after)
    if return_before:
        filters.append(Trip.expected_end_date <= return_before)
    if return_after:
        filters.append(Trip.expected_end_date >= return_after)

    if filters:
        trip = (db.query(Trip).filter(*filters)
                .filter(Trip.initiator_id.not_in(black_list) & (Trip.initiator_id != user_id)).first())
        if trip:
            return get_user_full(db, trip.initiator)
        else:
            return None
    else:
        res = db.query(User).filter(User.id.not_in(black_list) & (User.id != user_id)).first()
        if res:
            return get_user_full(db, res)
        else:
            return None

```