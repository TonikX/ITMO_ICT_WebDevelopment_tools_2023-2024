# endpoints/users.py

Необходимые импорты
```
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlmodel import select, Session
from datetime import datetime
from pydantic import BaseModel

from db.models import AppUser, AppUserDefault
from security.password_encoder import get_password_hash, verify_password
from connection import get_session
from .auth import get_current_user
```
```
router = APIRouter()
```
```
class ChangePassword(BaseModel):
    old_password: str
    new_password: str
```
```
class UserResponse(BaseModel):
    username: str
    email: str
    about: str
    location: str
```
```
@router.get("/", response_model=list[UserResponse])
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(AppUser)).all()

    user_responses = []
    for user in users:
        user_response = UserResponse(
            username=user.username,
            email=user.email,
            about=user.about,
            location=user.location,
        )
        user_responses.append(user_response)

    return user_responses
```
```
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(AppUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_response = UserResponse(
            username=user.username,
            email=user.email,
            about=user.about,
            location=user.location,
        )

    return user_response
```
```
@router.put("/", response_model=AppUser)
def update_user(user: AppUserDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    # Update the user's attributes
    current_user.username = user.username
    current_user.email = user.email
    current_user.about = user.about
    current_user.location = user.location
    current_user.last_updated_at = datetime.now()

    session.add(current_user)
    session.commit()
    return current_user
```
```
@router.post("/change_password", response_model=AppUser)
def update_user(change_password: ChangePassword, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    if not verify_password(change_password.old_password, current_user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    # Update the user's password
    current_user.password = get_password_hash(change_password.new_password)

    session.add(current_user)
    session.commit()

    return current_user
```
```
@router.delete("/")
def delete_user(session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):    
    session.delete(current_user)
    session.commit()
    return {"message": "User deleted"}
```