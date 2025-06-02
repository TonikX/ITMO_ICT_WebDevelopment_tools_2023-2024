from __future__ import annotations

from pydantic import BaseModel, HttpUrl, Field


class ParseAsyncCreate(BaseModel):
    url: HttpUrl = Field(..., example="https://example.com")


class ParseSyncQuery(BaseModel):
    url: HttpUrl = Field(..., example="https://example.com")