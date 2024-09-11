import typing as tp

from fastapi import Depends, HTTPException, status

from .database import AsyncSession, get_session
from .project import get_project
from .. import models


async def get_task(
    task_id: int,
    session: AsyncSession = Depends(get_session),
) -> models.Task:
    task = await session.get(models.Task, task_id)

    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    return task  # type: ignore


async def get_project_task(
    task: tp.Annotated[models.Task, Depends(get_task)],
    project: tp.Annotated[models.Project, Depends(get_project)],
) -> models.Task:
    if task.project_id != project.id:  # noqa
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Task not found")

    return task  # type: ignore
