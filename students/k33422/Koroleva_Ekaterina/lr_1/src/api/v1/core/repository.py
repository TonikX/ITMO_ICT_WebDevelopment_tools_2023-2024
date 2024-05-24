import typing as tp

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.core.types import ModelType
from src.services.pagination import PaginationParams


class BaseRepository:
    def __init__(
        self,
        model: ModelType,
        session_factory: tp.Callable[[], AsyncSession]
    ):
        self.model = model
        self.session_factory = session_factory

    async def create(
        self,
        data: dict
    ) -> ModelType:
        instance = self.model(**data)
        async with self.session_factory() as session:
            session.add(instance)
            await session.commit()
            await session.refresh(instance)
            return instance

    async def update(
        self,
        data: dict,
        **filters
    ) -> ModelType:
        statement = (
            update(self.model)
            .values(**data)
            .filter_by(**filters)
            .returning(self.model)
        )
        async with self.session_factory() as session:
            result = await session.execute(statement)
            await session.commit()
            return result.scalar_one()

    async def delete(
        self,
        **filters
    ) -> None:
        statement = delete(self.model).filter_by(**filters)
        async with self.session_factory() as session:
            await session.execute(statement)
            await session.commit()

    async def get_one(
        self,
        **filters
    ) -> ModelType | None:
        statement = select(self.model).filter_by(**filters)
        async with self.session_factory() as session:
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def get_many(
        self,
        pag_params: PaginationParams,
        **filters
    ) -> list[ModelType]:
        statement = (
            select(self.model)
            .filter_by(**filters)
            .limit(pag_params.limit)
            .offset(pag_params.offset)
        )
        async with self.session_factory() as session:
            result = await session.execute(statement)
            return result.scalars().all()

    async def exists(self, **filters) -> bool:
        result = await self.get_one(**filters)
        return result is not None


def change_model(
    model: ModelType
):
    def decorator(method):
        async def wrapper(self, *args, **kwargs):
            static_model = self.model
            self.model = model
            result = await method(self, *args, **kwargs)
            self.model = static_model
            return result

        return wrapper

    return decorator
