from fastapi import FastAPI, HTTPException, Depends, APIRouter
from psycopg2._psycopg import List
from sqlmodel import select
from models import User, UserInput, UserBase, UserLogin, UserReadFull, UserPassword
from auth.auth import AuthHandler
from database.conn import get_session

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/register', status_code=201, description='Register new user')
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
    return {"status": 201, "message": "New user is created!"}


@user_router.get('/users')
def get_users(session=Depends(get_session)) -> list[User]:
    users = session.exec(select(User)).all()
    return users


@user_router.post('/login')
def login(user: UserLogin, session=Depends(get_session)):
    user_found = session.exec(select(User).where(User.username == user.username)).first()
    if not user_found:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    verified = auth_handler.verify_password(user.password, user_found.password)
    if not verified:
        raise HTTPException(status_code=401, detail='Invalid username or password')
    token = auth_handler.encode_token(user_found.username)
    return {'token': token}


@user_router.get('/users/me')
def get_current_user(user: User = Depends(auth_handler.get_current_user)) -> UserReadFull:
    return user


@user_router.patch('/users/me/change-password')
def change_password(passwords: UserPassword, user: User = Depends(auth_handler.get_current_user),
                    session=Depends(get_session)):
    # Проверяем, что текущий пароль пользователя верный
    if not auth_handler.verify_password(passwords.old_password, user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    # Хешируем новый пароль
    hashed_new_password = auth_handler.get_password_hash(passwords.new_password)

    # Обновляем пароль пользователя в базе данных
    user.password = hashed_new_password
    session.add(user)
    session.commit()

    return {"message": "Password updated successfully"}


@user_router.get("/users/{user_id}")
def get_user_by_id(user_id: int, session=Depends(get_session)) -> UserReadFull:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
