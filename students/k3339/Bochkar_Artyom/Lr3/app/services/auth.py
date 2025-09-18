import datetime
import jwt
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlmodel import Session, select
from typing import Optional
from starlette import status

from app.db.conection import engine
from app.models.models import User
from app.services.hashing import verify_password

def get_user_by_username(username: str) -> Optional[User]:
    with Session(engine) as session:
        statement = select(User).where(User.username == username)
        return session.exec(statement).first()

class AuthHandler:
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    secret = 'supersecret'

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str, salt: str) -> bool:
        return verify_password(plain_password, hashed_password, salt)

    def encode_token(self, username: str):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(payload, self.secret, algorithm='HS256')

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired signature')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

    def get_current_user(self, auth: HTTPAuthorizationCredentials = Security(security)) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials'
        )
        username = self.decode_token(auth.credentials)
        if username is None:
            raise credentials_exception
        user = get_user_by_username(username)
        if user is None or not user.is_active:
            raise credentials_exception
        return user


async def get_current_user(auth_handler: AuthHandler = Depends(), 
        credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> User:
    return auth_handler.get_current_user(credentials)
