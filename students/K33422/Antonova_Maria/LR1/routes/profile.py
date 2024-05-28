import typing

from fastapi import APIRouter, Depends

from src.dependencies import get_current_user
from src.settings.connection import get_session
from src import models
from src.schemas.profile import ProfileUpdate
from src.adapters.db import SqlalchemyWorker
from sqlmodel import select

profile_route = APIRouter(prefix="/profile", tags=["profile"])


@profile_route.patch("/{id}", status_code=200)
def update_profile(
        profile_id: int, profile_update: ProfileUpdate, session=Depends(get_session),
        user=Depends(get_current_user)
):
    sqlalchemy_worker = SqlalchemyWorker(session)
    profile_query = select(models.Profile).where(models.Profile.id == profile_id, models.Profile.is_active == True)
    skills = profile_update.skills
    delattr(profile_update, "skills")
    updated_profile = sqlalchemy_worker.patch_object(profile_query, profile_update)
    skills_query = select(models.Skill).where(models.Skill.id.in_(skills))
    skills_profile = sqlalchemy_worker.get_objects(skills_query)
    for skill_profile in skills_profile:
        if skill_profile not in updated_profile.own_skills:
            updated_profile.own_skills.append(skill_profile)
    session.commit()
    session.refresh(updated_profile)

    profile = updated_profile.model_dump()
    profile["skills"] = updated_profile.own_skills

    return profile


@profile_route.delete("/{id}", status_code=204)
def deactivate_profile(profile_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> None:
    query = select(models.Profile).where(models.Profile.id == profile_id, models.Profile.is_active == True)
    SqlalchemyWorker(session).delete_object(query)


@profile_route.get("/{id}")
def get_profile(profile_id: int, session=Depends(get_session), user=Depends(get_current_user)) -> dict:
    query = ((select(models.Profile)
             .join(models.SkillsProfiles, models.SkillsProfiles.profile_id == models.Profile.id))
             .where(models.Profile.id == profile_id, models.Profile.is_active == True))

    profile = SqlalchemyWorker(session).get_object(query)
    profile_json = profile.model_dump()
    profile_json["skills"] = profile.own_skills
    return profile_json


@profile_route.get("/", response_model=typing.List[models.Profile])
def get_profiles(session=Depends(get_session), search: typing.Optional[str] = None,
                 user=Depends(get_current_user)) -> typing.List[models.Profile]:
    query = (select(models.Profile)
             .where(models.Profile.own_skills.any(models.Skill.name == search))) if search else select(models.Profile)
    return SqlalchemyWorker(session).get_objects(query)
