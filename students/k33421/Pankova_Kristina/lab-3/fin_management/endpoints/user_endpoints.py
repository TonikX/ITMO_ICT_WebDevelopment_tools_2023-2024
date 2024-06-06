from fastapi import APIRouter, HTTPException, Security, security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED,HTTP_404_NOT_FOUND
from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
import requests
from authentification.auth import AuthHandler
from db.connection import get_session
from models.user_models import UserInput, User, UserLogin
from repos.user_repos import select_all_users, find_user
from fastapi import APIRouter, HTTPException, status
from starlette.status import HTTP_200_OK
from typing import Dict
from celery import Celery

user_router = APIRouter()
auth_handler = AuthHandler()

@user_router.post('/registration', status_code=201, tags=['users'],
                  description='Register new user')
def register(user: UserInput):
    users = select_all_users()
    session = get_session()
    if any(x.username == user.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_pwd = auth_handler.get_password_hash(user.password)
    u = User(username=user.username, password=hashed_pwd, email=user.email,
             is_seller=user.is_seller)
    session.add(u)
    session.commit()
    return JSONResponse(status_code=HTTP_201_CREATED)


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
    return user

parser_router = APIRouter()

@parser_router.post("/parse", status_code=HTTP_200_OK)
def parse_url(url: str):
    try:
        # Send the URL to the parser container
        url = "http://parser:8001/parse"
        print(url)
        response = requests.post(url, json={"url": url})

        response.raise_for_status()

        # Return the response from the parser
        return JSONResponse(content=response.json())
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'


app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)
app.conf.update(from_object='config')

@app.task
def parse_url_cel(url):
    """
    Задача для парсинга URL в фоновом режиме.
    """
    print(f"Parsing URL: {url}")
    url = "http://parser:8001/parse"
    response = requests.post(url, json={"url": url})
    response.raise_for_status()
    return "Parsing completed"

@parser_router.post("/parse_celery", status_code=status.HTTP_200_OK)
async def parse_url(url: str) -> Dict[str, str]:
    try:
        # Отправляем задачу на выполнение в Celery
        task = parse_url_cel.delay(url)

        # Возвращаем ответ с информацией о начале выполнения задачи
        return {"task_id": task.id, "status": "Task started"}

    except Exception as e:
        raise Exception


