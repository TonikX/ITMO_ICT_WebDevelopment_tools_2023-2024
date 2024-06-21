from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from lab1.TeamTinder.connection import get_session
from lab1.TeamTinder.models import *


router = APIRouter()


@router.post("/user_project")
def user_project_create(user_project: UserProjectDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": UserProject}):
    user_project = UserProject.model_validate(user_project)
    session.add(user_project)
    session.commit()
    session.refresh(user_project)
    return {"status": 200, "data": user_project}


@router.get("/user_project/list", response_model=List[UserProjectExtended])
def user_project_list(session=Depends(get_session)) -> List[UserProject]:
    return session.exec(select(UserProject)).all()


@router.get("/user_project/{user_project_id}", response_model=UserProjectExtended)
def user_project_read(user_project_id: int, session=Depends(get_session)) -> UserProject:
    return session.get(UserProject, user_project_id)


@router.get("/user_project/list/user/{user_id}", response_model=List[UserProjectExtended])
def get_user_user_project(user_id: int, session=Depends(get_session)) -> List[UserProject]:
    query = select(UserProject).where(UserProject.user_id == user_id)
    user_projects = session.exec(query).all()
    if not user_projects:
        raise HTTPException(status_code=404, detail="User has no projects")

    return user_projects


@router.patch("/user_project/{user_project_id}")
def user_project_update(user_project_id: int, user_project: UserProjectPartialUpdate, session=Depends(get_session)) -> UserProject:
    db_user_project = session.get(UserProject, user_project_id)
    if not db_user_project:
        raise HTTPException(status_code=404, detail="User not found")
    user_project_data = user_project.model_dump(exclude_unset=True)
    for key, value in user_project_data.items():
        setattr(db_user_project, key, value)
    session.add(db_user_project)
    session.commit()
    session.refresh(db_user_project)
    return db_user_project


@router.delete("/user_project/{user_project_id}")
def user_project_delete(user_project_id: int, session=Depends(get_session)):
    user_project = session.get(UserProject, user_project_id)
    if not user_project:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user_project)
    session.commit()
    return {"ok": True}
