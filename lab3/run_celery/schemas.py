import datetime
from sqlmodel import Field, SQLModel


class Parse(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    article_title: str
