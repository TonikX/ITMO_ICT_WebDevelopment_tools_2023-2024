from fastapi import APIRouter, HTTPException, Depends
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

from auth import AuthHandler
from models.finance import Balance
from models.user import UserInput, User, UserLogin
from repositories.user import select_all_users, find_user, find_user_balance_id
from database import session

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.post('/registration', status_code=201, tags=['users'], description='Register new user')
def register(user: UserInput):
    users = select_all_users()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    balance = Balance(balance=0)
    balance.targets.extend([])
    balance.subscriptions.extend([])
    balance.transactions.extend([])
    user = User(username=user.username, password=hashed_pwd, email=user.email, balance=balance)
    session.add_all([user, balance])
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


@user_router.post('/users/me', tags=['users'])
def get_current_user(user: User = Depends(auth_handler.get_current_user)):
    return user

@user_router.get('/balance_id', tags=['users'])
def get_user_balance_id(user: User = Depends(auth_handler.get_current_user)):
    balance_id = find_user_balance_id(user.id)
    return {'balance_id': balance_id}