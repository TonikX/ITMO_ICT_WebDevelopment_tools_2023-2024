from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends

from app.services import Monolite
from connection import get_session


def get_monolite_server(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> Monolite:
    return Monolite(session)