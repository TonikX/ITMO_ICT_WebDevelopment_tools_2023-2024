import typing as tp

from fastapi import Depends, HTTPException, status

from .auntification import get_payload
from .database import AsyncSession, get_session
from .. import models, schemas


async def get_user(
    payload: tp.Annotated[schemas.Payload, Depends(get_payload)],
    session: AsyncSession = Depends(get_session),
) -> models.User:
    user = await session.get(models.User, payload.sub)

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")

    return user  # type: ignore
