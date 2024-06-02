from sqlmodel import Field, SQLModel

class Song(SQLModel, table=True):
    song_id: int = Field(primary_key=True)
    title: str
    author: str
    name: str