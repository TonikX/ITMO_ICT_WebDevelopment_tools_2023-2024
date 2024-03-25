from fastapi import APIRouter, Depends

from src.models import Team
from src.settings.connection import get_session
from src.adapters.db import SqlalchemyWorker
from src.schemas.team import TeamUpdate, TeamCreate, TeamParticipantUpdate
from sqlmodel import select
from src import models

team_route = APIRouter(prefix="/team", tags=["team"])


@team_route.post("/")
async def create_team(created_team: TeamCreate, session=Depends(get_session)):
    created_team.creator_id = 1
    team = Team.model_validate(created_team)
    return SqlalchemyWorker(session).create_object(team)


@team_route.get("/")
async def get_teams(session=Depends(get_session)):
    query = select(models.Team)
    return SqlalchemyWorker(session).get_objects(query)


@team_route.get("/{id}")
async def get_team(team_id: int, session=Depends(get_session)):
    query = select(models.Team).where(models.Team.id == team_id)
    return SqlalchemyWorker(session).get_object(query)


@team_route.patch("/{id}")
async def update_team(team_id: int, updated_team: TeamUpdate, session=Depends(get_session)):
    query = select(models.Team).where(models.Team.id == team_id)
    return SqlalchemyWorker(session).patch_object(query, updated_team)


@team_route.delete("/{id}")
async def delete_team(team_id: int, session=Depends(get_session)):
    query = select(models.Team).where(models.Team.id == team_id)
    SqlalchemyWorker(session).delete_object(query)


@team_route.post("/participant/add")
async def add_participant(updated_participant: TeamParticipantUpdate, session=Depends(get_session)):
    sqlalchemy_worker = SqlalchemyWorker(session)
    profile_query = (
        select(models.Profile)
        .where(models.Profile.id == updated_participant.profile_id, models.Profile.is_active == True))
    team_query = select(models.Team).where(models.Team.id == updated_participant.team_id)
    team = sqlalchemy_worker.get_object(team_query)
    profile = sqlalchemy_worker.get_object(profile_query)
    profile.team_id = team.id
    session.commit()
    return profile


@team_route.post("/participant/delete")
async def delete_participant(updated_participant: TeamParticipantUpdate, session=Depends(get_session)):
    sqlalchemy_worker = SqlalchemyWorker(session)
    profile_query = (
        select(models.Profile)
        .where(models.Profile.id == updated_participant.profile_id, models.Profile.is_active == True))
    team_query = select(models.Team).where(models.Team.id == updated_participant.team_id)
    team = sqlalchemy_worker.get_object(team_query)
    profile = sqlalchemy_worker.get_object(profile_query)
    profile.team_id = None
    session.commit()
    return profile
