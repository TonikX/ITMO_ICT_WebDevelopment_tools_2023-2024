from typing import Sequence, Type

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from auth import AuthHandler
from connection import get_session
from models.step_models import Step, StepDefault

step_router = APIRouter(tags=['Step'])
auth_handler = AuthHandler()


@step_router.get("/step/all")
def trip_list(session: Session = Depends(get_session)) -> Sequence[Step]:
    return session.exec(select(Step)).all()


@step_router.post("/step/create")
def create_step(step: StepDefault, session: Session = Depends(get_session)) -> Step:

    step = Step.model_validate(step)
    session.add(step)
    session.commit()
    session.refresh(step)
    return step


@step_router.delete("/step/delete")
def delete_step(step_id: int, session: Session = Depends(get_session
                                                                 )) -> Type[Step] | None:
    step = session.get(Step, step_id)
    session.delete(step)
    session.commit()
    return step
