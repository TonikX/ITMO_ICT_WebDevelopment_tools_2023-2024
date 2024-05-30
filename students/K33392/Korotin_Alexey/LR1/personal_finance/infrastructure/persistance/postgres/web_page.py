

from sqlmodel import SQLModel, Field


class WebPage(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field()
