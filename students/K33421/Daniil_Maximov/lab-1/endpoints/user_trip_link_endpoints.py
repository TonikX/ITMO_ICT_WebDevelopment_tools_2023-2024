from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing_extensions import List, TypedDict

from auth import AuthHandler
from connection import get_session
from exceptions.forbbiden_exception import ForbiddenException
from models.user_trip_link_models import UserTripLink, UserTripLinkDefault

user_trip_link_router = APIRouter(tags=['UserTripLinks'])
auth_handler = AuthHandler()


@user_trip_link_router.get("/usertrip/all")
def link_list(session: Session = Depends(get_session)) -> Sequence[UserTripLink]:
    return session.exec(select(UserTripLink)).all()


@user_trip_link_router.get("/usertrip/{user_id}in{trip_id}")
def link_one(user_id: int, trip_id: int, session=Depends(get_session)) -> UserTripLink:
    link = session.exec(
        select(UserTripLink).where(UserTripLink.user_id == user_id, UserTripLink.trip_id == trip_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="This user is not in this trip")
    return link


@user_trip_link_router.post("/usertrip/bind")
def link_create(link: UserTripLinkDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                      "data": UserTripLink}):
    if not (link.user_id == current.id or current.is_admin):
        raise ForbiddenException

    link = UserTripLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": link}

@user_trip_link_router.delete("/UserTripLink/delete/{user_id}in{trip_id}")
def link_delete(user_id: int, trip_id: int, session=Depends(get_session),
                current=Depends(auth_handler.current_user)):
    if not (user_id == current.id or current.is_admin):
        raise ForbiddenException

    link = session.exec(select(UserTripLink).where(UserTripLink.user_id == user_id and UserTripLink.trip_id == trip_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="This user is not in this trip")
    session.delete(link)
    session.commit()

    return {"status": 201, "message": f"deleted user {user_id} from trip {trip_id}"}