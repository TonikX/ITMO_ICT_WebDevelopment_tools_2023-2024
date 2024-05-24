from pydantic import BaseModel

from .mixins import SolidMixin


class Message(BaseModel, SolidMixin):
    msg: str
