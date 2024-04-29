from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.db import db_helper
from src.models import User
from .schemes import UserBase

__all__ = ['get_user']

from ..jwt import Payload, get_payload


async def get_user(
        payload: Annotated[Payload, Depends(get_payload)]
) -> UserBase:
    pk: int = int(payload.sub)

    async with db_helper.get_session() as session:
        user = await session.get(User, pk)

    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'User not found'
        )

    return UserBase.model_validate(user)
