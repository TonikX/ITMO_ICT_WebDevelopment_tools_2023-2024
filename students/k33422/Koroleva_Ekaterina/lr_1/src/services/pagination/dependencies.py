from typing import Annotated

from fastapi import (
    Query
)

from src.config import pag_settings
from .schemes import PaginationParams

__all__ = ['get_pagination_params']


def get_pagination_params(
    limit: Annotated[int, Query(ge=0, le=pag_settings.max_limit)] = pag_settings.max_limit,
    offset: Annotated[int, Query(ge=0)] = 0
) -> PaginationParams:
    return PaginationParams(
        limit=limit,
        offset=offset
    )
