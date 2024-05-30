import datetime
from fastapi import Security, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
import jwt
from starlette import status
from connection import get_session
from models import User
from sqlmodel import select


class AuthService:
    auth_scheme = HTTPBearer()
    pwd_context = CryptContext(schemes=['bcrypt'])
    SECRET_KEY = 'QWERTY12345'

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_token(self, username: str) -> str:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=8),
            'iat': datetime.datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm='HS256')

    def decode_token(self, token: str) -> str:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Expired token')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')

    def authenticate(self, auth: HTTPAuthorizationCredentials = Security(auth_scheme)) -> str:
        return self.decode_token(auth.credentials)

    def get_active_user(self, auth: HTTPAuthorizationCredentials = Security(auth_scheme),
                        session=Depends(get_session)) -> dict:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )
        username = self.decode_token(auth.credentials)
        if not username:
            raise credentials_exception

        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            raise credentials_exception

        return user.dict()
