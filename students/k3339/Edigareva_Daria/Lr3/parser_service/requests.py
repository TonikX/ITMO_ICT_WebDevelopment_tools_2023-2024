from __future__ import annotations

from pydantic import BaseModel, HttpUrl, Field


class FetchQuery(BaseModel):
    """Модель query‑параметра для /fetch."""

    url: HttpUrl = Field(..., example="https://example.com")