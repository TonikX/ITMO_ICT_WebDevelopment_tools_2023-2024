from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlmodel import select
from typing_extensions import TypedDict

from auth import AuthHandler
from db import get_session
from lib.models import User, UserProfile, UserDefault, UserWithProfile
from repos.users import find_user

users_router = APIRouter()
auth_handler = AuthHandler()


# ---- USERS ----
# @users_router.post("/users")
# def create_user_with_profile(user_data: UserDefault, profile_data: UserProfile,
#                              session=Depends(get_session)) -> User:
#     profile = UserProfile(**profile_data.dict())
#
#     session.add(profile)
#     session.commit()
#     session.refresh(profile)
#
#     user = User(**user_data.dict())
#
#     user.profile = profile
#
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#
#     return user


@users_router.get("/users")
def get_users(session=Depends(get_session)) -> List[User]:
    return session.exec(select(User)).all()


@users_router.patch("/users/{user_id}", response_model=User)
def update_user(user_id: int, profile_data: UserProfile, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get the user's existing profile
    profile = user.profile

    # Update profile data
    profile_data_dict = profile_data.dict(exclude_unset=True)
    for key, value in profile_data_dict.items():
        setattr(profile, key, value)

    session.commit()
    session.refresh(profile)
    return profile


@users_router.get('/users/me', response_model=UserWithProfile)
def get_current_user(user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)):
    userWithProfile = session.get(User, user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return userWithProfile


# Get User by ID
@users_router.get("/users/{user_id}", response_model=UserWithProfile)
def get_user(user_id: int, session=Depends(get_session)) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Delete User
@users_router.delete("/users/{user_id}")
def delete_user(user_id: int, session=Depends(get_session)) -> TypedDict('Response', {"message": str}):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}


@users_router.post('/registration')
def register(user_data: UserDefault, profile_data: UserProfile,
             session=Depends(get_session)) -> TypedDict('Response', {"status": int, "message": str}):
    users = session.exec(select(User)).all()
    if any(x.username == user_data.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user_data.password)
    profile = UserProfile(**profile_data.dict())

    session.add(profile)
    session.commit()
    session.refresh(profile)

    user = User(password=hashed_pwd, username=user_data.username)
    user.profile = profile

    session.add(user)
    session.commit()
    session.refresh(user)

    return {"status": 201, "message": "User created successfully"}


@users_router.post('/login')
def login(user: UserDefault) -> TypedDict('Response', {"token": str}):
    user_found = find_user(user.username)
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}
