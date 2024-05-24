from typing import Annotated

from pydantic import BaseModel, Field

from src.config import pag_settings
from src.core.pydantic.mixins import SolidUnionMixin

__all__ = ['PaginationParams']


class PaginationParams(BaseModel, SolidUnionMixin):
    limit: Annotated[int, Field(ge=0, le=pag_settings.max_limit)] = pag_settings.max_limit
    offset: Annotated[int, Field(ge=0)] = 0
