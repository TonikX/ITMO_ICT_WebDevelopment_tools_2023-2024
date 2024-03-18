from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select

from models.usertriplink_models import * 
from connection import *
from auth import AuthHandler


usertrip_router = APIRouter()
auth_handler = AuthHandler()


# all links
@usertrip_router.get("/usertrip/all", tags=['User-Trip Links'])
def link_list(session=Depends(get_session)) -> List[UserTripLink]:
    return session.exec(select(UserTripLink)).all()


# one link
@usertrip_router.get("/usertrip/{user_id}in{trip_id}", tags=['User-Trip Links'])
def link_one(user_id: int, trip_id: int, session=Depends(get_session)) -> UserTripLink:
    #return session.exec(select(Trip).where(Trip.id == trip_id)).first()
    link = session.exec(select(UserTripLink).where(UserTripLink.user_id == user_id, UserTripLink.trip_id == trip_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="This user is not in this trip")
    return link


# add link
@usertrip_router.post("/usertrip", tags=['User-Trip Links'])
def link_create(link: UserTripLinkDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                          "data":  UserTripLink}):
    if not (link.user_id == current.id or current.is_admin):
        raise HTTPException(status_code=403, detail="Forbidden action")
    link = UserTripLink.model_validate(link)
    session.add(link)
    session.commit()
    session.refresh(link)
    return {"status": 200, "data": link}


# delete link
@usertrip_router.delete("/UserTripLink/delete/{user_id}in{trip_id}", tags=['User-Trip Links'])
def link_delete(user_id: int, trip_id: int, session=Depends(get_session),
                current=Depends(auth_handler.current_user)):
    if not (user_id == current.id or current.is_admin):
        raise HTTPException(status_code=403, detail="Forbidden action")
    link = session.exec(select(UserTripLink).where(UserTripLink.user_id == user_id and UserTripLink.trip_id == trip_id)).first()
    if not link:
        raise HTTPException(status_code=404, detail="This user is not in this trip")
    session.delete(link)
    session.commit()
    return {"status": 201, "message": f"deleted user {user_id} from trip {trip_id}"}