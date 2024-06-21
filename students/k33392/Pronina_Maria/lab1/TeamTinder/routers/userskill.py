from fastapi import APIRouter, Depends, HTTPException
from typing_extensions import TypedDict
from sqlmodel import select

import sys
sys.path.append("../..")

from lab1.TeamTinder.connection import get_session
from lab1.TeamTinder.models import *


router = APIRouter()


@router.post("/user_skill")
def user_skill_create(user_skill: SkillUserLink, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": SkillUserLink}):
    user_skill = SkillUserLink.model_validate(user_skill)
    session.add(user_skill)
    session.commit()
    session.refresh(user_skill)
    return {"status": 200, "data": user_skill}


@router.get("/user_skill/list")
def user_skill_list(session=Depends(get_session)) -> List[SkillUserLink]:
    return session.exec(select(SkillUserLink)).all()


@router.get("/user_skill/{user_id}/{skill_id}")
def user_skill_read(user_id: int, skill_id: int, session=Depends(get_session)) -> SkillUserLink:
    query = select(SkillUserLink).where(SkillUserLink.user_id == user_id, SkillUserLink.skill_id == skill_id)
    result = session.exec(query)
    user_skill = result.one_or_none()
    if user_skill is None:
        raise HTTPException(status_code=404, detail="UserSkill not found")
    return user_skill


@router.patch("/user_skill/{user_id}/{skill_id}")
def user_skill_update(user_id: int, skill_id: int, user_skill: SkillUserLink, session=Depends(get_session)) -> SkillUserLink:
    query = select(SkillUserLink).where(SkillUserLink.user_id == user_id, SkillUserLink.skill_id == skill_id)
    result = session.exec(query)
    db_user_skill = result.one_or_none()
    if not db_user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")

    user_skill_data = user_skill.model_dump(exclude_unset=True)
    for key, value in user_skill_data.items():
        setattr(db_user_skill, key, value)

    session.add(db_user_skill)
    session.commit()
    session.refresh(db_user_skill)
    return db_user_skill


@router.delete("/user_skill/{user_id}/{skill_id}")
def user_skill_delete(user_id: int, skill_id: int, session=Depends(get_session)):
    query = select(SkillUserLink).where(SkillUserLink.user_id == user_id, SkillUserLink.skill_id == skill_id)
    result = session.exec(query)
    user_skill = result.one_or_none()
    if not user_skill:
        raise HTTPException(status_code=404, detail="UserSkill not found")

    session.delete(user_skill)
    session.commit()
    return {"ok": True}
