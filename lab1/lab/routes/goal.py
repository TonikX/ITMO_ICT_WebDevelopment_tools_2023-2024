from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Goal

router = APIRouter()

@router.get("/goals", response_model=List[Goal], tags=["goal"])
def get_goals(session=Depends(get_session)) -> List[Goal]:
    return session.exec(select(Goal)).all()

@router.get("/goals/{goal_id}", response_model=Goal, tags=["goal"])
def get_goal(goal_id: int, session=Depends(get_session)) -> Goal:
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

@router.post("/goals", response_model=Goal, tags=["goal"])
def create_goal(goal: Goal, session=Depends(get_session)) -> Goal:
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal

@router.patch("/goals/{goal_id}", response_model=Goal, tags=["goal"])
def update_goal(goal_id: int, goal: Goal, session=Depends(get_session)) -> Goal:
    db_goal = session.get(Goal, goal_id)
    if not db_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    goal_data = goal.dict(exclude_unset=True)
    for key, value in goal_data.items():
        setattr(db_goal, key, value)
    session.add(db_goal)
    session.commit()
    session.refresh(db_goal)
    return db_goal

@router.delete("/goals/{goal_id}", tags=["goal"])
def delete_goal(goal_id: int, session=Depends(get_session)):
    goal = session.get(Goal, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    session.delete(goal)
    session.commit()
    return {"ok": True}