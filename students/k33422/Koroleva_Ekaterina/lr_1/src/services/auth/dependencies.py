from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.db import db_helper
from src.models import User
from ..jwt import get_payload, Payload

__all__ = ['get_user', 'get_user_profile', 'get_superuser']


async def get_user(
    payload: Annotated[Payload, Depends(get_payload)]
) -> User:
    pk: int = int(payload.sub)

    statement = (
        select(User)
        .where(User.id == pk)
        .options(selectinload(User.profile))
    )
    async with db_helper.get_session() as session:
        result = await session.execute(statement)
        user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'User not found'
        )

    if not user.is_active:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            'User is not active'
        )

    return user


async def get_user_profile(
    user: Annotated[User, Depends(get_user)]
) -> User:
    if user.profile is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Profile not found'
        )

    return user


async def get_superuser(
    user: Annotated[User, Depends(get_user)]
) -> User:
    if not user.is_superuser:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            'User is not superuser'
        )

    return user
