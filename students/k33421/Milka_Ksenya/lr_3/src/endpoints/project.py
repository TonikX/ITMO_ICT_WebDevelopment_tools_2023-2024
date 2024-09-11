import typing as tp

from fastapi import APIRouter, Depends
from sqlmodel import select

from .. import dependencies, models, queue, schemas

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("")
async def get_projects(
    payload: tp.Annotated[schemas.Payload, Depends(dependencies.get_payload)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
    is_active: tp.Optional[bool] = None,
):
    statement = select(models.Project)
    if is_active is not None:
        statement = statement.where(models.Project.is_active == is_active)  # noqa
    project_result = await session.exec(statement)
    projects = project_result.all()

    return list(map(schemas.Project.model_validate, projects))


@router.post("/{project_id}/join", response_model=str)
async def join_project(
    schema: schemas.ProjectJoin,
    project: tp.Annotated[models.Project, Depends(dependencies.get_project)],
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    project_user = models.ProjectUser(**schema.model_dump(), project_id=project.id, user_id=user.id)
    session.add(project_user)
    await session.commit()

    return "OK"


@router.post("/upload", response_model=schemas.Queue)
async def upload_projects(
    schema: schemas.ProjectUpload,
    user: tp.Annotated[models.User, Depends(dependencies.get_user)],
):
    task = queue.upload_new_projects.delay(schema.page)
    return schemas.Queue(id=task.id, status=task.status, result=task.result)


@router.get("/upload/{queue_id}", response_model=schemas.Queue)
async def get_upload_status(
    queue_id: str,
):
    task = queue.upload_new_projects.AsyncResult(queue_id)
    return schemas.Queue(id=task.id, status=task.status, result=task.result)
