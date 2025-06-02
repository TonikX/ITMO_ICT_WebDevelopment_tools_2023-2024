from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, HttpUrl

from status_enum import StatusEnum


class ParseAsyncResponse(BaseModel):
    request_id: int
    status: StatusEnum


class StatusResponse(BaseModel):
    request_id: int
    status: StatusEnum


class ResultResponse(BaseModel):
    request_id: int
    status: StatusEnum
    title: Optional[str] = None
    html: Optional[str] = None


class SyncResult(BaseModel):
    title: str
    html: str
    url: HttpUrl