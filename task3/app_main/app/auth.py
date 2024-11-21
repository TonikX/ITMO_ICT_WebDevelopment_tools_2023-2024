from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError
from pathlib import Path
from dotenv import dotenv_values
import datetime
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
import db_queries

#dotenv setup
env_path = Path(__file__).parent / '.env'
config = dotenv_values(env_path)
# jwt setup
SECRET_KEY = config['JWT_SECRET_KEY']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 800000
# hasher setup
crypto_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
# auth scheme setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(provided_password, actual_hash):
    return crypto_context.verify(provided_password, actual_hash)


def get_password_hash(password):
    return crypto_context.hash(password)


def generate_token(username):
    to_encode = {
        'exp': datetime.datetime.now() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        ),
        'iat': datetime.datetime.now(),
        'sub': username
    }
    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def decode_token(token):
    try: 
        
        decoded_token = jwt.decode(
            token,
            SECRET_KEY,
            ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail='Invalid token. Invalid format'
        )
    return decoded_token
"""
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTk5MTUxMTcsImlhdCI6MTcxMTkxNTExNywic3ViIjoidXNlcjEifQ.CdzMds38zLe9hw3EBuwxAGUT2FvoRbdTDVSE-tnW0aQ
"""

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return get_user_by_token(token)


def get_user_by_token(token):
    token_data = decode_token(token)
    username = token_data['sub']
    try: 
        user = db_queries.get_user_by_username(username)
    except ValueError:
        raise HTTPException(
            status_code=403,
            detail='Invalid token. No such user'
        )
    return user
