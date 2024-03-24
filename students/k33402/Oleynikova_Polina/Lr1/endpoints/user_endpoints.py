from fastapi import APIRouter, HTTPException, Depends
from starlette.status import HTTP_201_CREATED
from auth.auth import AuthHandler
from db.connection import get_session
from models import UserInput, User, UserLogin, UserPassword, UserReadFull
from sqlmodel import select


user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201, description='Register new user')
def register(user: UserInput, session=Depends(get_session)):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    if any(x.email == user.email for x in users):
        raise HTTPException(status_code=400, detail='Email is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd, email=user.email, name=user.name, about=user.about)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


@user_router.post('/login')
def login(user: UserLogin, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@user_router.get('/users/me')
def get_current_user(user: User = Depends(auth_handler.get_current_user)) -> UserReadFull:
    return user


@user_router.patch("/users/me/password")
def user_pwd(user_pwd: UserPassword, session=Depends(get_session), current=Depends(auth_handler.get_current_user)):
    found_user = session.get(User, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    verified = auth_handler.verify(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = auth_handler.get_password_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}


@user_router.get("/users")
def user_list(session=Depends(get_session)) -> list[User]:
    users = session.exec(select(User)).all()
    user_models = [user.model_dump(exclude={'password'}) for user in users]
    return user_models


@user_router.get("/users/{user_id}")
def user_one(user_id: int, session=Depends(get_session)) -> UserReadFull:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user