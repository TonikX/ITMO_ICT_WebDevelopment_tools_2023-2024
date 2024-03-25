import typing

from pydantic import BaseModel


class ProfileUpdate(BaseModel):
    description: typing.Optional[str]
    skills: typing.List[typing.Optional[int]]
