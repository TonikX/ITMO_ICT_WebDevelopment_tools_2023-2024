from __future__ import annotations

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models import ParseRequest
from status_enum import StatusEnum


class ParseRepository:
    """Инкапсулирует доступ к таблице parse_requests."""

    @staticmethod
    async def create(session: AsyncSession, url: str) -> ParseRequest:
        req = ParseRequest(url=url, status=StatusEnum.pending)
        session.add(req)
        await session.commit()
        await session.refresh(req)
        return req

    @staticmethod
    async def by_id(session: AsyncSession, request_id: int) -> ParseRequest | None:
        res = await session.execute(select(ParseRequest).where(ParseRequest.id == request_id))
        return res.scalar_one_or_none()

    @staticmethod
    async def update_status(
        session: AsyncSession,
        request_id: int,
        status: StatusEnum,
        *,
        title: str | None = None,
        html: str | None = None,
    ) -> None:
        stmt = (
            update(ParseRequest)
            .where(ParseRequest.id == request_id)
            .values(status=status, title=title, html_content=html)
        )
        await session.execute(stmt)
        await session.commit()