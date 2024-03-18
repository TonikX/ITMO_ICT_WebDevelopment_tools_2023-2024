from auth.auth import AuthHandler
from connection import init_db, get_session
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import select 
from models import *
from typing_extensions import TypedDict

router = APIRouter()
auth_handler = AuthHandler()

# Profiles endpoint

@router.get('/profile/{profile_id}', tags=["profiles"])
def profile_get(profile_id: int, session=Depends(get_session)) -> ProfileReviews:
    profile = session.query(UserProfile).filter(UserProfile.id == profile_id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    reviews = session.query(UserReview).filter(UserReview.user_profile_id == profile_id).all()
    profile = ProfileReviews(**profile.dict(), reviews=reviews)
    
    return profile

@router.post('/profile', tags=["profiles"])
def profile_create(profile: UserProfileDefault, current_user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": UserProfile}): # type: ignore
    # Assign the current user's ID to the profile
    profile_dict = profile.dict()
    profile_dict["user_id"] = current_user.id

    # Create a new profile instance with the assigned user_id
    profile_instance = UserProfile(**profile_dict)

    # Add the profile to the session
    session.add(profile_instance)
    session.commit()
    session.refresh(profile_instance)
    
    return {"status": 200, "data": profile}


@router.delete('/profile/delete', tags=["profiles"])
def profile_delete(user: User = Depends(auth_handler.get_current_user),
                   session=Depends(get_session)):

    if not user.user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    session.delete(user.user_profile)
    session.commit()
    return {"ok": True}

@router.patch("/profile", tags=["profiles"])
def profile_update(profile: UserProfileDefault, 
                   user: User = Depends(auth_handler.get_current_user), 
                   session=Depends(get_session)) -> UserProfileDefault:
    if not user.user_profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    profile_data = profile.dict(exclude_unset=True)
    for key, value in profile_data.items():
        setattr(user.user_profile, key, value)
    
    session.add(user.user_profile)
    session.commit()
    session.refresh(user.user_profile)
    return user.user_profile