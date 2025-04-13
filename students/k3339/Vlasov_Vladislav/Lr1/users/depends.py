from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from users.service import UserService
from connection import get_session


def get_user_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserService:
    return UserService(session)