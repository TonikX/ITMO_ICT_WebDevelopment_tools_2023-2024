import fastapi
from fastapi import HTTPException
from starlette import status

from src.adapters.auth import AuthHandler
from src.repos.auth import find_user


def get_current_user(token: str = fastapi.Header("token")):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    username = AuthHandler().decode_token(token)
    if username is None:
        raise credentials_exception
    user = find_user(username)
    if user is None:
        raise credentials_exception
    return user
