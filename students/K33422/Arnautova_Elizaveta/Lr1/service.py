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
