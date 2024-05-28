from fastapi import APIRouter
from typing import List
from pr1.models import Profile, temp_bd, User

router = APIRouter(prefix="/profile")



@router.get("/", summary="Returns the list of profiles")
def get_profile_list() -> List[Profile]:
    return temp_bd

@router.get("/{id}")
def profile(id: int) -> Profile:
    return [profile for profile in temp_bd if profile.get("id") == id][0]


@router.post("/")
def profile_create(profile: Profile):
    profile_to_append = profile.model_dump()
    temp_bd.append(profile_to_append)
    return {"status": 201, "data": profile}


@router.delete("/{id}")
def profile_delete(id: int):
    for i, profile in enumerate(temp_bd):
        if profile.get("id") == id:
            temp_bd.pop(i)
            break
    return {"status": 204, "message": "deleted"}


@router.put("/{id}")
def profile_update(id: int, profile: Profile):
    for num, raw in enumerate(temp_bd):
        if raw.get("id") == id:
            temp_bd.pop(num)
            temp_bd.append(profile.model_dump())
            return profile
    return {"status": 404, "message": "Not found"}


@router.get("/{id}/user")
def user(id: int) -> User:
    profile = [profile for profile in temp_bd if profile.get("id") == id][0]
    return User(**profile.get("user"))


@router.delete("/{id}/skills")
def delete_skills(id: int):
    for i, raw in enumerate(temp_bd):
        if raw.get("id") == id:
            raw.pop("skills")
            break
    return {"status": 204, "message": "deleted"}
