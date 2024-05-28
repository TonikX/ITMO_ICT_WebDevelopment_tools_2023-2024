import typing

from fastapi import APIRouter, Depends
from sqlmodel import select

from src.adapters.db import SqlalchemyWorker
from src.models import Project, Team, Skill, Profile
from src.schemas.project import ProjectCreate
from src.settings.connection import get_session

project_route = APIRouter(prefix="/project", tags=["project"])


@project_route.post("/", response_model=Project, status_code=201)
async def create_project(created_project: ProjectCreate, session=Depends(get_session)) -> Project:
    sqlalchemy_worker = SqlalchemyWorker(session)
    team_query = select(Team).where(Team.id == created_project.team_id, Team.is_active == True)
    sqlalchemy_worker.get_object(team_query)
    project = Project.model_validate(created_project)

    return sqlalchemy_worker.create_object(project)


@project_route.patch("/{id}", response_model=Project)
async def update_project(project_id: int, created_project: ProjectCreate, session=Depends(get_session)) -> Project:
    sqlalchemy_worker = SqlalchemyWorker(session)
    query = select(Project).where(Project.id == project_id, Project.is_active == True)
    team_query = select(Team).where(Team.id == created_project.team_id, Team.is_active == True)
    sqlalchemy_worker.get_object(team_query)

    return SqlalchemyWorker(session).patch_object(query, created_project)


@project_route.delete("/{id}", status_code=204)
async def delete_project(project_id: int, session=Depends(get_session)) -> None:
    query = select(Project).where(Project.id == project_id, Project.is_active == True)

    SqlalchemyWorker(session).delete_object(query)


@project_route.get("/{id}")
async def get_project(project_id: int, session=Depends(get_session)) -> dict:
    sqlalchemy_worker = SqlalchemyWorker(session)
    query = select(Project).where(Project.id == project_id, Project.is_active == True)

    project = sqlalchemy_worker.get_object(query)
    project_members_query = select(Profile).where(project.team_id == Profile.team_id)
    project_members = sqlalchemy_worker.get_objects(project_members_query)
    project = project.model_dump()
    project["members"] = project_members

    return project


@project_route.get("/", response_model=typing.List[Project])
async def get_projects(session=Depends(get_session), search: typing.Optional[str] = None) -> typing.List[Project]:
    query = select(Project).where(Project.requirements_skills.any(Skill.name == search)) if search else select(Project)

    return SqlalchemyWorker(session).get_objects(query)
