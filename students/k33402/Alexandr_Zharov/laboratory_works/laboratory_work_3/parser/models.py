from pydantic import BaseModel
from sqlmodel import SQLModel, Field, create_engine, Session
from typing import Optional

class UrlRequest(BaseModel):
    url: str

class TitleResponse(BaseModel):
    id: int
    url: str
    title: str

class Article(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    url: str
    title: str
