# JWT Auth

Для авторизации и создания токенов были выделены отдельные методы в слое приложения

## JWT
```python
import datetime
import os

import jwt
from dotenv import load_dotenv
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status

from personal_finance.application.ioc import IocContainer
from personal_finance.application.users.dto import ReadUserDto
from personal_finance.application.users.service import UserService

load_dotenv()

security = HTTPBearer()
secret = os.getenv('JWT_SECRET')


def encode_token(user_id: int) -> str:
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
        'iat': datetime.datetime.utcnow(),
        'sub': user_id
    }
    return jwt.encode(payload, secret, algorithm='HS256')


def decode_token(token: str) -> int:
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return int(payload['sub'])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail='Expired signature')
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail='Invalid token')


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)) -> int:
    return decode_token(auth.credentials)


def get_current_user(auth: HTTPAuthorizationCredentials = Security(security),
                     user_service: UserService = Depends(IocContainer.service['UserService'])) -> ReadUserDto:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    user_id = decode_token(auth.credentials)
    if user_id is None:
        raise credentials_exception
    user = user_service.find_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user
```

## Хэширование паролей
Функционал был вынесен в отедельные функции в слое приложения. Для повышения безопасности использовались 
hash salt и hash pepper.
```python
from passlib.context import CryptContext
from dotenv import load_dotenv
import os
pwd_context = CryptContext(schemes=['bcrypt'])
SALT = os.getenv('SALT')
PEPPER = os.getenv('PEPPER')
load_dotenv()


def get_password_hash(password: str) -> str:
    return pwd_context.hash(f'{SALT}{password}{PEPPER}'.encode())


def verify_password(pwd:  str, hashed_pwd: bytes | str) -> bool:
    return pwd_context.verify(f'{SALT}{pwd}{PEPPER}', hashed_pwd)
```