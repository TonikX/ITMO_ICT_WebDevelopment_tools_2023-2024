from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from starlette.responses import JSONResponse
from app.core import db
from app.models.auth import Token
from app.models.main import Balance
from app.models.user import (
    UserChangePassword,
    UserInput,
    User,
    UserLogin,
    UserMeResponse,
    UserRegisterResponse,
)
from app.services.user import select_all_users, find_user
import app.services.auth as auth_service

router = APIRouter()


@router.post(
    "/register",
    status_code=201,
    response_model=UserRegisterResponse,
    description="Register new user",
)
def register(
    user_data: UserInput, session: Session = Depends(db.get_session)
) -> UserRegisterResponse:
    users = select_all_users()
    if any(x.username == user_data.username for x in users):
        raise HTTPException(status_code=400, detail="Username is taken")
    hashed_pwd = auth_service.get_password_hash(user_data.password)
    balance = Balance(balance=0)
    user = User(
        username=user_data.username,
        password=hashed_pwd,
        email=user_data.email,
        balance=balance,
    )
    session.add_all([user, balance])
    session.commit()
    session.refresh(user)

    token = auth_service.encode_token(user.username)

    return UserRegisterResponse(
        username=user.username,
        created_at=user.created_at,
        email=user.email,
        id=user.id,
        token=Token(access_token=token),
    )


@router.post("/login", response_model=Token)
def login(user: UserLogin) -> Token:
    user_found = find_user(user.username)

    if not user_found:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")
    verified = auth_service.verify_password(user.password, user_found.password)

    if not verified:
        raise HTTPException(status_code=401, detail="Invalid username and/or password")

    token = auth_service.encode_token(user_found.username)
    return Token(access_token=token)


@router.post("/me", response_model=UserMeResponse)
def get_current_user(
    user: User = Depends(auth_service.get_current_user),
) -> UserMeResponse:
    return UserMeResponse(
        username=user.username,
        created_at=user.created_at,
        email=user.email,
        id=user.id,
    )


@router.post("/change_password")
def change_password(
    user_data: UserChangePassword,
    user: User = Depends(auth_service.get_current_user),
    session: Session = Depends(db.get_session),
) -> JSONResponse:
    hashed_pwd = auth_service.get_password_hash(user_data.password)
    user.password = hashed_pwd
    session.add(user)
    session.commit()
    session.refresh(user)

    return JSONResponse(
        status_code=200, content={"detail": "Password successfully updated"}
    )
