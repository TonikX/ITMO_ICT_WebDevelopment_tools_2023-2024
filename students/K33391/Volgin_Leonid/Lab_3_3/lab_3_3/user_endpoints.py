from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from auth.auth import AuthHandler
from models.main_models import User

from models.user_models import UserInput, UserLogin
from repos.user_repos import select_all_users, find_user
from db import db_session as session

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201, tags=['users'], description='Register new user')
def register(user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    description = "New user"
    u = User(username=user.username, password=hashed_pwd, email=user.email, description=description)
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

@user_router.get("/pwd_change")
def fresh_pwd(pwd, new_pwd, user=Depends(auth_handler.get_current_user)):
    hashed_pwd = auth_handler.get_password_hash(pwd)
    #print(hashed_pwd)
    #print(user.password)
    #if hashed_pwd == user.password:
    new_hashed_pwd = auth_handler.get_password_hash(new_pwd)
    session.query(User).filter(User.id == user.id).update({'password': new_hashed_pwd})
    session.commit()
    #else:
        #raise HTTPException(status_code=401, detail=f'{hashed_pwd} {user.password}')



@user_router.post('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user.username