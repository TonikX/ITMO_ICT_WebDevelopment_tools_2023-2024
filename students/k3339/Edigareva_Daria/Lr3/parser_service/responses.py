from __future__ import annotations

from pydantic import BaseModel, HttpUrl


class FetchResponse(BaseModel):
    url: HttpUrl
    title: str
    html: str