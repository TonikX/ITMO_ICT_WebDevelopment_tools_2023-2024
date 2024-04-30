from typing import Annotated

from fastapi import (
    Query
)

from .schemes import FilterParams, SearchParam

__all__ = ['get_filter_params', 'get_search_param']


def get_filter_params(
    start_location: Annotated[str | None, Query()] = None,
    destination: Annotated[str | None, Query()] = None,
) -> FilterParams:
    return FilterParams(
        start_location=start_location,
        destination=destination
    )


def get_search_param(
    search: Annotated[str | None, Query()] = None
) -> SearchParam:
    return SearchParam(
        search=search
    )
