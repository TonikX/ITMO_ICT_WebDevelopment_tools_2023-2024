from connection import get_session
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from sqlmodel import select 
from models import *
import datetime
from decouple import config

JWT_SECRET = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)
    
    def verify_password(self, pwd, hashed_pwd):
        return self.pwd_context.verify(pwd, hashed_pwd)
    
    def encode_token(self, user_id):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired siganture')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
        
    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)
    
    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security), session=Depends(get_session)):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        
        user = session.exec(select(User).where(User.username == username)).first()
        if user is None:
            raise credentials_exception
        return user