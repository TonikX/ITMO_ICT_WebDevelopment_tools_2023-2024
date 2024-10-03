from fastapi import APIRouter, Depends
from db import get_session
from typing import List, NotRequired
from typing_extensions import TypedDict
from sqlmodel import select
from models.project import *

router = APIRouter()


@router.get("/project")
def projects_get(session = Depends(get_session)) -> List[ProjectOut]:
    statement = select(Project).order_by(Project.id)
    return session.exec(statement).all()


@router.post("/project")
def project_post(project: ProjectDefault, session = Depends(get_session)) -> TypedDict("Response", {"status": int, "data": NotRequired[Project]}):
    project = Project.model_validate(project)
    session.add(project)
    session.commit()
    session.refresh(project)
    return {"status": 201, "data": project}


@router.put("/project/{project_id}")
def project_put(project: ProjectDefault, project_id: int, session=Depends(get_session)) -> TypedDict("Response", {"status": int, "data": NotRequired[Project]}):
    project_to_update = session.get(Project, project_id)
    if not project_to_update:
        return {"status": 404}
    project_data = project.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        setattr(project_to_update, key, value)
    session.add(project_to_update)
    session.commit()
    session.refresh(project_to_update)
    return {"status": 201, "data": project_to_update}


@router.delete("/project/{project_id}")
def task_delete(project_id: int, session=Depends(get_session)) -> TypedDict("Response", {"status": int, "data":NotRequired[Project]}):
    project_to_delete = session.get(Project, project_id)
    if not project_to_delete:
        return {"status": 404}
    session.delete(project_to_delete)
    session.commit()
    return {"status": 201, "data": project_to_delete}
