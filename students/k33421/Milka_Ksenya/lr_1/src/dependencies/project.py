import typing as tp

from fastapi import Depends, HTTPException, status
from sqlmodel import select

from .database import AsyncSession, get_session
from .user import get_user
from .. import models


async def get_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
) -> models.Project:
    project = await session.get(models.Project, project_id)

    if project is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    return project  # type: ignore


async def get_created_project(
    project: tp.Annotated[models.Project, Depends(get_project)],
    user: tp.Annotated[models.User, Depends(get_user)],
) -> models.Project:
    if project.creator_id != user.id:  # noqa
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    return project  # type: ignore


async def get_member_project(
    project: tp.Annotated[models.Project, Depends(get_project)],
    user: tp.Annotated[models.User, Depends(get_user)],
    session: AsyncSession = Depends(get_session),
) -> models.Project:
    result = await session.exec(
        select(models.ProjectUser)
        .where(models.ProjectUser.project_id == project.id)  # noqa
        .where(models.ProjectUser.user_id == user.id),  # noqa
    )
    project_user = result.one_or_none()

    if project_user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Project not found")

    return project  # type: ignore
