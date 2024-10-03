from fastapi import APIRouter, Depends
from db import get_session
from typing import List, NotRequired
from typing_extensions import TypedDict
from sqlmodel import select
from models.priority import *

router = APIRouter()


@router.get("/priority", response_model=List[Priority])
def priority_get(session=Depends(get_session)):
    statement = select(Priority)
    result = session.exec(statement).all()
    # if not result:
    #     return {"status": 404}
    # return {"status": 200, "data": result}
    return result


@router.post("/priority")
def priority_post(priority: PriorityDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority = Priority.model_validate(priority)
    session.add(priority)
    session.commit()
    session.refresh(priority)
    return {"status": 201, "data": priority}


@router.get("/priority/{priority_id}")
def priority_get_by_id(priority_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority = session.get(Priority, priority_id)
    if not priority:
        return {"status": 404}
    return {"status": 200, "data": priority}


@router.put("/priority/{priority_id}")
def priority_update(priority_id: int, priority: PriorityDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority_to_update = session.get(Priority, priority_id)
    if not priority_to_update:
        return {"status": 404}
    priority_data = priority.model_dump(exclude_unset=True)
    for key, value in priority_data.items():
        setattr(priority_to_update, key, value)
    session.add(priority_to_update)
    session.commit()
    session.refresh(priority_to_update)
    return {"status": 201, "data": priority_to_update}


@router.delete("/priority/{priority_id}")
def priority_update(priority_id: int, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Priority]}):
    priority_to_delete = session.get(Priority, priority_id)
    if not priority_to_delete:
        return {"status": 404}
    session.delete(priority_to_delete)
    session.commit()
    return {"status": 201, "data": priority_to_delete}