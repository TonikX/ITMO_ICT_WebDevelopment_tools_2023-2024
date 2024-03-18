from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select

from models.transition_models import * 
from connection import *
from auth import AuthHandler


transition_router = APIRouter()
auth_handler = AuthHandler()


# all transitions
@transition_router.get("/transition/all", tags=['Transitions'])
def transition_list(session=Depends(get_session)) -> List[Transition]:
    return session.exec(select(Transition)).all()


# one transition
@transition_router.get("/transition/{transition_id}", tags=['Transitions'])
def transition_one(transition_id: int, session=Depends(get_session)) -> Transition:
    #return session.exec(select(Transition).where(Transition.id == transition_id)).first()
    transition = session.get(Transition, transition_id)
    if not transition:
        raise HTTPException(status_code=404, detail="Transition not found")
    return transition


# add transition
@transition_router.post("/transition", tags=['Transitions'])
def transition_list(transition: TransitionDefault, session=Depends(get_session),
                    current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                                           "data": Transition}):
    transition = Transition.model_validate(transition)
    session.add(transition)
    session.commit()
    session.refresh(transition)
    return {"status": 200, "data": transition}


# delete transition
@transition_router.delete("/transition/delete/{transition_id}", tags=['Transitions'])
def transition_delete(transition_id: int, session=Depends(get_session),
                      current=Depends(auth_handler.current_user)):
    if not current.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    transition = session.get(Transition, transition_id)
    if not transition:
        raise HTTPException(status_code=404, detail="Transition not found")
    session.delete(transition)
    session.commit()
    return {"status": 201, "message": f"deleted transition with id {transition_id}"}


# update transition
@transition_router.patch("/transition/edit/{transition_id}", tags=['Transitions'])
def transition_update(transition_id: int, transition: TransitionDefault, session=Depends(get_session),
                      current=Depends(auth_handler.current_user)) -> Transition:
    if not current.is_admin:
        raise HTTPException(status_code=403, detail="Only admin can perform this action")
    db_transition = session.get(Transition, transition_id)
    if not db_transition:
        raise HTTPException(status_code=404, detail="Transition not found")
    transition_data = transition.model_dump(exclude_unset=True)
    for key, value in transition_data.items():
        setattr(db_transition, key, value)
    session.add(db_transition)
    session.commit()
    session.refresh(db_transition)
    return db_transition