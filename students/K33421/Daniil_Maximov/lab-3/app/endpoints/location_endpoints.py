from typing import Sequence, Type

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from auth import AuthHandler
from connection import get_session
from models.location_models import Location, LocationDefault

location_router = APIRouter(tags=['Location'])
auth_handler = AuthHandler()


@location_router.get("/location/all")
def trip_list(session: Session = Depends(get_session)) -> Sequence[Location]:
    return session.exec(select(Location)).all()


@location_router.post("/location/create")
def create_location(location: LocationDefault, session: Session = Depends(get_session)) -> Location:

    location = Location.model_validate(location)
    session.add(location)
    session.commit()
    session.refresh(location)
    return location


@location_router.delete("/location/delete")
def delete_location(location_id: int, session: Session = Depends(get_session
                                                                 )) -> Type[Location] | None:
    location = session.get(Location, location_id)
    session.delete(location)
    session.commit()
    return location
