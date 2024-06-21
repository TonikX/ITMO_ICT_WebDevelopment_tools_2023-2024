from sqlmodel import SQLModel, Field

class WebPage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str
    title: str
