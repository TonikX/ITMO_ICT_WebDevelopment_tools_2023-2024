from typing import Optional
from pydantic import BaseModel, HttpUrl


class URLData(BaseModel):
    url: HttpUrl


class ArticlesParseResponse(BaseModel):
    ok: bool
    task_id: Optional[str]
