import typing as tp

from sqlmodel import Field, SQLModel


class IDMixin(SQLModel):
    id: tp.Optional[int] = Field(None, primary_key=True)
