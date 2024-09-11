from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from auth.auth import AuthHandler
from models.user_models import UserInput, UserLogin

from repos.user_repos import select_all_users, find_user
from db import db_session as session


from models.travel_models import User, User_Submodel

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201, tags=['users'])
def register(user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hashed_pwd, email=user.email)
    session.add(u)
    session.commit()

    return JSONResponse(status_code=201, content={"message": "User registered successfully"})


@user_router.post('/login', tags=['users'])
def login(user: UserLogin):
    user_found = find_user(user.username)

    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)

    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')

    token = auth_handler.encode_token(user_found.username)
    return {'token': token}

@user_router.get("/password_change")
def fresh_pwd(new_pwd, user=Depends(auth_handler.get_current_user)):
    new_hashed_pwd = auth_handler.get_password_hash(new_pwd)
    session.query(User).filter(User.id == user.id).update({'password': new_hashed_pwd})
    session.commit()

@user_router.post('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user.username

@user_router.get("/user_info",response_model=User_Submodel)
def get_user_info(user=Depends(auth_handler.get_current_user)):
    u = session.get(User, user.id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u