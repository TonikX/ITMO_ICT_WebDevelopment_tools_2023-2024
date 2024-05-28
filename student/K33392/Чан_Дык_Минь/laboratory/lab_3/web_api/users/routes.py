from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from web_api.auth.auth import AuthHandler
from web_api.connection import init_db, get_session
from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel import select 
from web_api.models import *
from typing_extensions import TypedDict

router = APIRouter()
auth_handler = AuthHandler()

# Users Endpoints
@router.post('/registration', tags=["users"])
def register(user: UserInput, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": User}): # type: ignore
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail="Username is already exist")
    hash_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hash_pwd, email=user.email)
    session.add(u)
    session.commit()
    return {"status": 200, "data": user}

@router.post('/login', tags=["users"])
def login(user: UserLogin, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@router.get('/user/me', tags=["users"], response_model=Profile_User)
def get_current_user(user: User = Depends(auth_handler.get_current_user), session=Depends(get_session)):
    profile = session.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    profile_user = Profile_User(**user.dict(), profile=profile)
    return profile_user

@router.get('/users', tags=["users"], response_model=List[Profile_User])
def get_all_users(session=Depends(get_session)):
    users = session.exec(select(User)).all()
    profile_users = []
    
    for user in users:
        profile = session.exec(select(UserProfile).where(UserProfile.user_id == user.id)).first()
        profile_user = Profile_User(**user.dict(), profile=profile)
        profile_users.append(profile_user)
    
    return profile_users


@router.delete('/user/delete{user_id}', tags=["users"])
def user_delete(user_id: UUID, session=Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

@router.patch("/user", tags=["users"])
def user_update(password_change: UserChangePassWord, 
                user: User = Depends(auth_handler.get_current_user), 
                session=Depends(get_session)) -> UserDefault:
    # Verify old password
    if not auth_handler.verify_password(password_change.old_password, user.password):
        raise HTTPException(status_code=400, detail="Invalid old password")

    # Validate new password
    if len(password_change.new_password) < 6:
        raise HTTPException(status_code=400, detail="New password must be at least 6 characters long")

    # Update password
    user.password = auth_handler.get_password_hash(password_change.new_password)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

