from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import Enum, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from status_enum import StatusEnum


class Base(DeclarativeBase):
    pass


class ParseRequest(Base):
    """Таблица запросов на парсинг."""

    __tablename__ = "parse_requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    status: Mapped[StatusEnum] = mapped_column(Enum(StatusEnum), default=StatusEnum.pending)
    title: Mapped[Optional[str]]
    html_content: Mapped[Optional[str]]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now(),
    )