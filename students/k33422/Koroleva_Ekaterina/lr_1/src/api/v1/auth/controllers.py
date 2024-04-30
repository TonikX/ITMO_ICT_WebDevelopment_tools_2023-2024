from typing import Annotated

from fastapi import (APIRouter, Body, Depends, HTTPException, status)

from src.core.pydantic.schemes import Message
from src.models import User
from src.services.auth import get_user
from src.services.encrypt import hash_password, validate_password
from src.services.jwt import create_jwt, JWT
from .repository import repository
from .schemes import (PasswordChange, UserCredentials, UserPrivate)

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login/', response_model=Annotated[JWT, Depends()])
async def login(
    credentials: Annotated[UserCredentials, Body()]
):
    user = await repository.get_one(email=credentials.email)

    if not (
            user and
            validate_password(credentials.password, user.hashed_password)
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid credentials'
        )

    return create_jwt(user)


@router.post('/register/', response_model=Annotated[UserPrivate, Depends()])
async def register(
    credentials: Annotated[UserCredentials, Body()]
):
    is_exists = await repository.exists(email=credentials.email)

    if is_exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Email already registered'
        )

    return await repository.create(
        dict(
            email=credentials.email,
            hashed_password=hash_password(credentials.password)
        )
    )


@router.post('/change-password/', response_model=Annotated[Message, Depends()])
async def change_password(
    data: Annotated[PasswordChange, Body()],
    user: Annotated[User, Depends(get_user)]
):
    if not validate_password(
        data.old_password,
        user.hashed_password
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Invalid old password'
        )

    await repository.update(
        dict(
            hashed_password=hash_password(data.new_password)
        ),
        id=user.id
    )

    return Message(msg='Success')
