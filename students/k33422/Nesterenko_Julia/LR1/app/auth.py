import datetime

from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt

import os
from dotenv import load_dotenv
load_dotenv()

from .connection import *
from .models.user_models import * 


class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = os.getenv('SECRET')

    # хэширование пароля
    def get_hash(self, password):
        return self.pwd_context.hash(password)

    # валидация пароля
    def verify(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd, scheme='bcrypt')
    
    # генерация токена
    def encode_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')
    
    # декодирование токена
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Signature expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail=f"Invalid token")
    
    # получение текущего пользователя в сессии
    def current_user(self, auth: HTTPAuthorizationCredentials = Security(security), 
                     session=Depends(get_session)) -> User:
        id = self.decode_token(auth.credentials)
        if not id:
            raise HTTPException(status_code=401, detail="User not authorized")
        db_user = session.get(User, id)
        if not db_user:
            raise HTTPException(status_code=401, detail="User not authorized")
        return db_user