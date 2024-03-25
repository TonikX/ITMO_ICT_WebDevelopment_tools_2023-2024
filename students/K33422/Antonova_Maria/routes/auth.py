from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from starlette.responses import JSONResponse

from src.adapters.auth import AuthHandler
from src.adapters.db import SqlalchemyWorker
from src.dependencies import get_current_user
from src.models import User
from src.schemas.auth import UserLogin, ChangePasswordSchema
from src.settings.connection import get_session

auth_route = APIRouter(prefix="/auth", tags=["auth"])
auth_handler = AuthHandler()


@auth_route.post("/login")
def login(user_login: UserLogin, session=Depends(get_session)):
    query = select(User)
    users = SqlalchemyWorker(session).get_objects(query)[0]
    if not users:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user_login.password, users.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(users.username)
    return {'token': token}


@auth_route.post("/register")
def register(user_register: UserLogin, session=Depends(get_session)):
    sqlalchemy_worker = SqlalchemyWorker(session)
    query = select(User)
    users = sqlalchemy_worker.get_objects(query)
    if any(x.username == user_register.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user_register.password)
    user = User(username=user_register.username, password=hashed_pwd)
    session.add(user)
    session.commit()
    return JSONResponse(status_code=201, content={"message": "Registered"})


@auth_route.post("/change_password", status_code=200)
def change_password(
        change_password_schema: ChangePasswordSchema,
        session=Depends(get_session),
        user=Depends(get_current_user)
):
    hashed_pwd = auth_handler.get_password_hash(change_password_schema.new_password)
    user.password = hashed_pwd
    session.add(user)
    session.commit()
    return JSONResponse(status_code=200, content={"message": "Password has been changed"})
