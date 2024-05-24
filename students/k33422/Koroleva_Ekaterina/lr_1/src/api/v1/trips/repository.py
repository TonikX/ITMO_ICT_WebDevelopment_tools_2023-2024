from sqlalchemy import or_, select
from sqlalchemy.orm import selectinload

from src.db import db_helper
from src.models import Participant, Profile, Trip
from src.services.pagination import PaginationParams
from .filters import FilterParams, SearchFields, SearchParam
from ..core.repository import BaseRepository, change_model


class TripsRepository(BaseRepository):
    def __init__(
        self,
        search_fields: list[str],
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.search_fields = search_fields

    async def get_many_trips_filters(
        self,
        pag_params: PaginationParams,
        filter_params: FilterParams,
        search_param: SearchParam,
        **filters
    ) -> list[Trip]:
        statement = (
            select(self.model)
            .filter_by(**filter_params.model_dump(exclude_none=True), **filters)
            .limit(pag_params.limit)
            .offset(pag_params.offset)
        )

        if search_param.search:
            search_filters = [
                getattr(self.model, i).ilike(f'%{search_param.search}%')
                for i in self.search_fields
            ]
            statement = statement.filter(or_(*search_filters))

        statement = statement.options(
            selectinload(self.model.profile)
            .selectinload(Profile.user)
        )

        async with self.session_factory() as session:
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_one_trip(
        self,
        **filters
    ):
        statement = (
            select(self.model)
            .filter_by(**filters)
            .options(
                selectinload(self.model.profile)
                .selectinload(Profile.user),
                selectinload(self.model.participants)
            )
        )
        async with self.session_factory() as session:
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    @change_model(Participant)
    async def create_participant(
        self,
        data: dict
    ):
        return await self.create(data)


repository = TripsRepository(
    search_fields=list(SearchFields),
    model=Trip,
    session_factory=db_helper.get_session
)
