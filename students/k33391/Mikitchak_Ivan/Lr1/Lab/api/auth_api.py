from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from models import LoginForm, LoginResponse, User
from connection import get_session
from utilities import create_access_token, get_user_by_token, verify_password

from dependencies import oauth2_scheme


router = APIRouter()

# Login (by JWT)
@router.post("/auth/login")
def login(request: LoginForm,
          session: Session = Depends(get_session)) -> LoginResponse:
    user = session.exec(select(User).where(User.email == request.email)).one_or_none()

    if user is None or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

    token = create_access_token(data={"sub": user.id})

    return LoginResponse(access_token=token, token_type="bearer")


# Logout (invalidate all issued JWT-s)
@router.post("/auth/logout")
def logout(token: Optional[str] = Depends(oauth2_scheme),
           session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    user.last_logout = datetime.now().astimezone()
    session.add(user)
    session.commit()
