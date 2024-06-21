from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from connection import get_session
from models import *


router = APIRouter()


@router.post("/team")
def team_create(team: TeamDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Team}):
    team = Team.model_validate(team)
    session.add(team)
    session.commit()
    session.refresh(team)
    return {"status": 200, "data": team}


@router.get("/team/list", response_model=List[TeamExtended])
def team_list(session=Depends(get_session)) -> List[Team]:
    return session.exec(select(Team)).all()


@router.get("/team/{team_id}", response_model=TeamExtended)
def team_read(team_id: int, session=Depends(get_session)) -> Team:
    return session.get(Team, team_id)


@router.patch("/team/{team_id}", response_model=TeamExtended)
def team_update(team_id: int, team: TeamPartialUpdate, session=Depends(get_session)) -> Team:
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="User not found")
    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/team/{team_id}")
def team_delete(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(team)
    session.commit()
    return {"ok": True}
