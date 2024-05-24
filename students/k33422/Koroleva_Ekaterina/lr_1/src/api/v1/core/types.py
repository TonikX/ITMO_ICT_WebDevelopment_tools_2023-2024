import typing as tp

from pydantic import BaseModel

from src.models import Base

ModelType = tp.TypeVar('ModelType', bound=Base)
SchemeType = tp.TypeVar('SchemeType', bound=BaseModel)
