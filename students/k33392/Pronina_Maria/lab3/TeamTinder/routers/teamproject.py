from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from connection import get_session
from models import *


router = APIRouter()


@router.post("/team_project")
def team_project_create(team_project: TeamProjectDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": TeamProject}):
    team_project = TeamProject.model_validate(team_project)
    session.add(team_project)
    session.commit()
    session.refresh(team_project)
    return {"status": 200, "data": team_project}


@router.get("/team_project/list", response_model=List[TeamProjectExtended])
def team_project_list(session=Depends(get_session)) -> List[TeamProject]:
    return session.exec(select(TeamProject)).all()


@router.get("/team_project/{team_project_id}", response_model=TeamProjectExtended)
def team_project_read(team_project_id: int, session=Depends(get_session)) -> TeamProject:
    return session.get(TeamProject, team_project_id)


@router.patch("/team_project/{team_project_id}")
def team_project_update(team_project_id: int, team_project: TeamProjectPartialUpdate, session=Depends(get_session)) -> TeamProject:
    db_team_project = session.get(TeamProject, team_project_id)
    if not db_team_project:
        raise HTTPException(status_code=404, detail="Team Project not found")

    team_project_data = team_project.model_dump(exclude_unset=True)
    for key, value in team_project_data.items():
        setattr(db_team_project, key, value)
    session.add(db_team_project)
    session.commit()
    session.refresh(db_team_project)
    return db_team_project


@router.delete("/team_project/{team_project_id}")
def team_project_delete(team_project_id: int, session=Depends(get_session)):
    team_project = session.get(TeamProject, team_project_id)
    if not team_project:
        raise HTTPException(status_code=404, detail="Team Project not found")
    session.delete(team_project)
    session.commit()
    return {"ok": True}
