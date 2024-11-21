import datetime

import jose.jwt
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated, Union
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt


class PasswordHandler:
    crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(self, provided_password, actual_hash):
        return self.crypto_context.verify(provided_password, actual_hash)

    def get_password_hash(self, password):
        return self.crypto_context.hash(password)


class TokenHandler:
    SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 800

    def generate_token(self, username):
        to_encode = {
            'exp': datetime.datetime.now() + datetime.timedelta(
                minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
            'iat': datetime.datetime.now(),
            'sub': username
        }
        return jwt.encode(
            to_encode,
            self.SECRET_KEY,
            algorithm=self.ALGORITHM
        )

    def decode_token(self, token):
        return jwt.decode(
            token,
            self.SECRET_KEY,
            self.ALGORITHM
        )


class UserHandler:
    def get_user_by_token(self, token):
        token_data = token_handler.decode_token(token)
        username = token_data['sub']
        return self.get_user_by_username(username)

    def get_user_by_username(self, username: str):
        username = username
        users = [user for user in fake_db if user.username == username]
        if not users:
            raise HTTPException(status_code=404, detail='incorrect username')
        user = users[0]
        return user


password_handler = PasswordHandler()
token_handler = TokenHandler()
user_handler = UserHandler()



class User(BaseModel):
    username: str
    password_hash: str
    age: int

fake_db = [
    User(username='seva', password_hash=password_handler.get_password_hash('786811'), age=21),
    User(username='anton', password_hash=password_handler.get_password_hash('123456'), age=25)
]


auther = OAuth2PasswordBearer('/token')
app = FastAPI()


@app.post('/token/')
def get_token(login_info: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = user_handler.get_user_by_username(login_info.username)
    if not password_handler.verify_password(login_info.password, user.password_hash):
        raise HTTPException(status_code=401, detail='incorrect password')
    token = token_handler.generate_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(token: Annotated[str, Depends(auther)]):
    return user_handler.get_user_by_token(token)


@app.get('/user/info')
def user_info(user: Annotated[User, Depends(get_current_user)]):
    return user.model_dump()