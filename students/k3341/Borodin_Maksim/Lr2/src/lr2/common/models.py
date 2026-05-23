from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class ParsedPage(SQLModel, table=True):
    __tablename__ = "parsed_pages"

    id: Optional[int] = Field(default=None, primary_key=True)
    url: str = Field(max_length=2048, index=True)
    title: str | None = Field(default=None, max_length=512)
    status: str = Field(max_length=20)
    concurrency_mode: str = Field(max_length=20, index=True)
    http_status_code: int | None = None
    error_message: str | None = Field(default=None, max_length=500)
    duration_ms: int | None = Field(default=None, ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
