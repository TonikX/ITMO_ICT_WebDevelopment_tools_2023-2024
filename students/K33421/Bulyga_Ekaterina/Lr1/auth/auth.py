from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from sqlmodel import Session

from models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class UserManager:
    def create_user(self, session: Session, user: User):
        db_user = session.get(User, user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        hashed_password = pwd_context.hash(user.hashed_password)
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()

    def get_user(self, session: Session, username: str):
        return session.get(User, username)

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def change_password(self, session: Session, username, new_password):
        user = self.get_user(session, username)
        user.hashed_password = pwd_context.hash(new_password)
        session.add(user)
        session.commit()
        session.refresh(user)
