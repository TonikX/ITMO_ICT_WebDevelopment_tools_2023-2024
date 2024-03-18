from fastapi import APIRouter, Depends, HTTPException
from typing import List
from typing_extensions import TypedDict
from sqlmodel import select

from models.step_models import * 
from connection import *
from auth import AuthHandler
from endpoints.trip_endpoints import user_in_members


step_router = APIRouter()
auth_handler = AuthHandler()


# all steps
@step_router.get("/step/all", response_model=List[StepDetailed], tags=['Steps (Trip-Stay/Transition Links)'])
def step_list(session=Depends(get_session)) -> List[Step]:
    return session.exec(select(Step)).all()


# one step
@step_router.get("/step/{step_id}", response_model=StepDetailed, tags=['Steps (Trip-Stay/Transition Links)'])
def step_one(step_id: int, session=Depends(get_session)) -> Step:
    #return session.exec(select(Step).where(Step.id == step_id)).first()
    step = session.get(Step, step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    return step


# add step
@step_router.post("/step", tags=['Steps (Trip-Stay/Transition Links)'])
def step_create(step: StepDefault, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> TypedDict('Response', {"status": int,
                                                                                  "data": Step}):
    if not (current.is_admin or user_in_members(step.trip_id, current.id)):
        raise HTTPException(status_code=403, detail="You have no access to this trip")
    step_data = step.model_dump(exclude_unset=True)
    if ((step_data.get("stay_id") == 0 and step_data.get("transition_id") == 0) 
    or (step_data.get("stay_id") != 0 and step_data.get("transition_id") != 0)):
        raise HTTPException(status_code=400, detail="Invalid data")
    if step_data.get("stay_id") == 0:
        step.stay_id = None
    if step_data.get("transition_id") == 0:
        step.transition_id = None
    step = Step.model_validate(step)
    session.add(step)
    session.commit()
    session.refresh(step)
    return {"status": 200, "data": step}


# delete step
@step_router.delete("/step/delete/{step_id}", tags=['Steps (Trip-Stay/Transition Links)'])
def step_delete(step_id: int, session=Depends(get_session),
                current=Depends(auth_handler.current_user)):
    step = session.get(Step, step_id)
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")
    if not (current.is_admin or user_in_members(step.trip_id, current.id)):
        raise HTTPException(status_code=403, detail="You have no access to this trip")
    session.delete(step)
    session.commit()
    return {"status": 201, "message": f"deleted step with id {step_id}"}


# update step
@step_router.patch("/step/edit/{step_id}", tags=['Steps (Trip-Stay/Transition Links)'])
def step_update(step_id: int, step: Step, session=Depends(get_session),
                current=Depends(auth_handler.current_user)) -> Step:
    db_step = session.get(Step, step_id)
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")
    if not (current.is_admin or user_in_members(step.trip_id, current.id)):
        raise HTTPException(status_code=403, detail="You have no access to this trip")
    step_data = step.model_dump(exclude_unset=True)
    for key, value in step_data.items():
        setattr(db_step, key, value)
    session.add(db_step)
    session.commit()
    session.refresh(db_step)
    return db_step