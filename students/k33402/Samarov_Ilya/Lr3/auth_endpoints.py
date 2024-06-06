from fastapi import APIRouter
from auth import *
from database import get_session
from models import UserBase, User, UserShow, ChangePassword, UserCreate
from sqlmodel import select


auth_router = APIRouter()


@auth_router.post('/registration', status_code=201, description='Register new user')
def register(user: UserCreate, session=Depends(get_session)):
    users = session.exec(select(User)).all()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = get_password_hash(user.password)
    user = User(username=user.username, password=hashed_pwd)
    session.add(user)
    session.commit()
    return {"status": 201, "message": "Created"}


@auth_router.post('/login')
def login(user: UserBase, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    verified = verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = encode_token(user_found.username)
    return {'token': token}


@auth_router.get('/me', response_model=UserShow)
def get_current_user(user: User = Depends(get_current_user)) -> User:
    return user


@auth_router.patch("/me/change-password")
def user_pwd(user_pwd: ChangePassword, session=Depends(get_session), current=Depends(get_current_user)):
    found_user = session.get(User, current.id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    verified = verify_password(user_pwd.old_password, found_user.password)
    if not verified:
        raise HTTPException(status_code=400, detail="Invalid old password")
    hashed_pwd = get_password_hash(user_pwd.new_password)
    found_user.password = hashed_pwd
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    return {"status": 200, "message": "password changed successfully"}
