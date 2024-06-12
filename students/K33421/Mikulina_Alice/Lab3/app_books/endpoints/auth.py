from fastapi import Depends, FastAPI, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import BaseModel

from db.models import AppUser, AppUserDefault
from security.password_encoder import oauth2_scheme, verify_password, get_password_hash
from security.jwt_process import create_access_token, parse_jwt_token
from connection import get_session


router = APIRouter()

class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


async def get_current_user(session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)):
    user_id = parse_jwt_token(token)

    user = session.get(AppUser, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/token", response_model=Token)
def login(user_credits: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user: AppUser = session.exec(select(AppUser).filter(AppUser.username == user_credits.username)).first()

    if user is None:
        raise HTTPException(status_code=404, detail="Username not found")

    if not verify_password(user_credits.password, user.password):
        raise HTTPException(status_code=404, detail="Incorrect password")

    token = create_access_token({"sub": user.id})
    return Token(access_token=token)


@router.post("/register", response_model=Token)
def register(new_user: AppUserDefault, session: Session = Depends(get_session)):
    user: AppUser = session.exec(select(AppUser).filter(AppUser.username == new_user.username)).first()

    if user is not None:
        raise HTTPException(status_code=404, detail="Username already taken")

    db_user = AppUser(
        username=new_user.username,
        email=new_user.email,
        password=get_password_hash(new_user.password),
        about=new_user.about,
        location=new_user.location,
    )
    session.add(db_user)
    session.commit()

    token = create_access_token({"sub": db_user.id})
    return Token(access_token=token)
