from enum import Enum

from pydantic import BaseModel

from src.core.pydantic.mixins import SolidMixin

__all__ = ['FilterParams', 'SearchParam', 'SearchFields']


class FilterParams(BaseModel, SolidMixin):
    start_location: str | None = None,
    destination: str | None = None,


class SearchParam(BaseModel, SolidMixin):
    search: str | None = None


class SearchFields(str, Enum):
    TITLE = 'title'
    DESCRIPTION = 'description'
    START_LOCATION = 'start_location'
    DESTINATION = 'destination'
