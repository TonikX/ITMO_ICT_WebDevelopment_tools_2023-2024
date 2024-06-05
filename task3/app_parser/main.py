# from parser_threading.main import main
from parser_threading.main import main
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from typing import Annotated
import requests
from tasks import parse_task

import os


if "BACKEND_URL" not in os.environ:
    raise RuntimeError('environment variable "BACKEND_URL" is not set')
BACKEND_URL = os.environ["BACKEND_URL"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()



@app.get('/')
def parse_data(token: Annotated[str, Depends(oauth2_scheme)]):
    response = check_backend_connection(token)
    check_token(response)
    try:
        parse_task.delay(token)
    except Exception as e:
        raise HTTPException(
            status_code=501, 
            detail='Server error while parsing: \n'+ str(e)
        )
    return {'msg': 'Процесс парсинга запустился, подождите 10 секунд'}


def check_backend_connection(token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    try:
        response = requests.get(
            f'{BACKEND_URL}/user/', 
            headers=headers)
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=404, 
            detail=f'Invalid variable BACKEND_URL or backend is down. BACKEND_URL:{BACKEND_URL}'
        )
    return response

def check_token(response):
    status_code = response.status_code
    if status_code == 403:
        raise HTTPException(status_code=403, detail='Invalid token') 
    elif status_code == 404:
        raise HTTPException(
            status_code=404, 
            detail=f'Invalid variable BACKEND_URL or backend is unreachable. BACKEND_URL:{BACKEND_URL}'
        )