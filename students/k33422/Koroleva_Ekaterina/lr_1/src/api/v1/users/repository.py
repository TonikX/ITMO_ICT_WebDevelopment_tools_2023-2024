from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.db import db_helper
from src.models import Profile, User
from src.services.pagination import PaginationParams
from ..core.repository import BaseRepository, change_model


class UsersRepository(BaseRepository):
    @change_model(User)
    async def get_many_users(
        self,
        pag_params: PaginationParams,
        **filters
    ) -> list[User]:
        return await self.get_many(
            pag_params=pag_params,
            **filters
        )

    @change_model(User)
    async def get_one_user(
        self,
        **filters
    ) -> User | None:
        statement = select(self.model).filter_by(**filters).options(
            selectinload(self.model.profile)
        )
        async with self.session_factory() as session:
            result = await session.execute(statement)
            return result.scalar_one_or_none()


repository = UsersRepository(
    model=Profile,
    session_factory=db_helper.get_session
)
