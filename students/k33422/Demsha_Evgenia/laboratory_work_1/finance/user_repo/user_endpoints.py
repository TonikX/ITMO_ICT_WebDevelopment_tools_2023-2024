from fastapi import APIRouter, HTTPException, Depends
from user_repo.auth import AuthHandler
from sqlalchemy.orm import Session
from connections import get_session
from user_repo.user_models import UserInput, User, UserLogin, UserPasswordChange
from user_repo.user_functions import select_all_users, find_user

user_router = APIRouter()
auth_handler = AuthHandler()


@user_router.post('/registration', status_code=201, tags=['users'],
                  description='Register new user')
def register(user: UserInput, session: Session = Depends(get_session)):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hashed_pwd, email=user.email)
    session.add(u)
    session.commit()
    # return JSONResponse(content="Registration successful", status_code=HTTP_201_CREATED)
    return {"message": "Registration successful"}


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


@user_router.get('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return {"id": user.id, "username": user.username, "email": user.email, "is_admin": user.is_admin}


@user_router.get("/users", tags=['users'])
async def get_all_users(session: Session = Depends(get_session),
                        user=Depends(auth_handler.get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")

    users = session.query(User).all()
    return {"users": [user.dict() for user in users]}


@user_router.put("/users/change_password", tags=['users'])
async def change_user_password(user_update: UserPasswordChange, session: Session = Depends(get_session),
                               user=Depends(auth_handler.get_current_user)):

    # db_user = session.query(User).filter(User.id == user.id).first()
    db_user = session.get(User, user.id)

    if not auth_handler.verify_password(user_update.old_password, db_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect.")

    db_user.password = auth_handler.get_password_hash(user_update.new_password)
    session.commit()

    return {"message": "Password changed successfully."}
