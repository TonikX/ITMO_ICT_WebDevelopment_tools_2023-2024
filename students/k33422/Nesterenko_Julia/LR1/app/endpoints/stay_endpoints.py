from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select


from app.models.stay_models import * 
from app.connection import *
from app.auth import AuthHandler


stay_router = APIRouter()
auth_handler = AuthHandler()


# all stays
@stay_router.get("/stay/all", tags=['Stays'])
def stay_list(session=Depends(get_session)) -> List[Stay]:
    return session.exec(select(Stay)).all()


# one stay
@stay_router.get("/stay/{stay_id}", tags=['Stays'])
def stay_one(stay_id: int, session=Depends(get_session)) -> Stay:
    #return session.exec(select(Stay).where(Stay.id == stay_id)).first()
    stay = session.get(Stay, stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail="Stay not found")
    return stay


# add stay
@stay_router.post("/stay", tags=['Stays'])
def stay_create(stay: StayDefault, session=Depends(get_session), 
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                           "data": Stay}):
    stay = Stay.model_validate(stay)
    session.add(stay)
    session.commit()
    session.refresh(stay)
    return {"status": 200, "data": stay}


# delete stay
@stay_router.delete("/stay/delete/{stay_id}", tags=['Stays'])
def stay_delete(stay_id: int, session=Depends(get_session),
                current=Depends(auth_handler.current_user)):
    if not current.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    stay = session.get(Stay, stay_id)
    if not stay:
        raise HTTPException(status_code=404, detail="Stay not found")
    session.delete(stay)
    session.commit()
    return {"status": 201, "message": f"deleted stay with id {stay_id}"}


# update stay
@stay_router.patch("/stay/edit/{stay_id}", tags=['Stays'])
def stay_update(stay_id: int, stay: StayDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> Stay:
    if not current.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    db_stay = session.get(Stay, stay_id)
    if not db_stay:
        raise HTTPException(status_code=404, detail="Stay not found")
    stay_data = stay.model_dump(exclude_unset=True)
    for key, value in stay_data.items():
        setattr(db_stay, key, value)
    session.add(db_stay)
    session.commit()
    session.refresh(db_stay)
    return db_stay