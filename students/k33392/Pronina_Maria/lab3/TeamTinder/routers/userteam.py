from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from connection import get_session
from models import *


router = APIRouter()


@router.post("/user_team")
def user_team_create(user_team: TeamUserLink, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": TeamUserLink}):
    user_team = TeamUserLink.model_validate(user_team)
    session.add(user_team)
    session.commit()
    session.refresh(user_team)
    return {"status": 200, "data": user_team}


@router.get("/user_team/list")
def user_team_list(session=Depends(get_session)) -> List[TeamUserLink]:
    return session.exec(select(TeamUserLink)).all()


@router.get("/user_team/{user_id}/{team_id}")
def user_team_read(user_id: int, team_id: int, session=Depends(get_session)) -> TeamUserLink:
    query = select(TeamUserLink).where(TeamUserLink.user_id == user_id, TeamUserLink.team_id == team_id)
    result = session.exec(query)
    user_team = result.one_or_none()
    if user_team is None:
        raise HTTPException(status_code=404, detail="UserTeam not found")
    return user_team


@router.patch("/user_team/{user_id}/{team_id}")
def user_team_update(user_id: int, team_id: int, user_team: TeamUserLinkPartialUpdate, session=Depends(get_session)) -> TeamUserLink:
    query = select(TeamUserLink).where(TeamUserLink.user_id == user_id, TeamUserLink.team_id == team_id)
    result = session.exec(query)
    db_user_team = result.one_or_none()
    if not db_user_team:
        raise HTTPException(status_code=404, detail="UserTeam not found")

    user_team_data = user_team.model_dump(exclude_unset=True)
    for key, value in user_team_data.items():
        setattr(db_user_team, key, value)

    session.add(db_user_team)
    session.commit()
    session.refresh(db_user_team)
    return db_user_team


@router.delete("/user_team/{user_id}/{team_id}")
def user_team_delete(user_id: int, team_id: int, session=Depends(get_session)):
    query = select(TeamUserLink).where(TeamUserLink.user_id == user_id, TeamUserLink.team_id == team_id)
    result = session.exec(query)
    user_team = result.one_or_none()
    if not user_team:
        raise HTTPException(status_code=404, detail="UserTeam not found")

    session.delete(user_team)
    session.commit()
    return {"ok": True}
