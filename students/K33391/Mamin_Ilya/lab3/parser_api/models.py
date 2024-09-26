from sqlmodel import SQLModel, Field

class Article(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    url: str
    text: str