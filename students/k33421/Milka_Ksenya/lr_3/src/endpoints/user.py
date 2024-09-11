import typing as tp

from fastapi import APIRouter, Depends
from sqlalchemy import orm
from sqlmodel import select

from .. import dependencies, models, schemas

router = APIRouter(prefix="/client", tags=["Client & Projects"])


@router.get("/me", response_model=schemas.UserMe)
async def get_me(
    user: models.User = Depends(dependencies.get_user),
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    created_projects_result = await session.exec(select(models.Project).where(models.Project.creator_id == user.id))  # noqa
    created_projects = created_projects_result.all()

    user_skills_result = await session.exec(
        (
            select(models.UserSkill)
            .where(models.UserSkill.user_id == user.id)  # noqa
            .options(orm.joinedload(models.UserSkill.skill))  # type: ignore  # noqa
        )
    )
    user_skills = user_skills_result.all()

    return schemas.UserMe.model_validate(
        dict(
            **user.model_dump(),
            created_projects=created_projects,
            skills=[
                dict(
                    **user_skill.skill.model_dump(),
                    level=user_skill.level,
                )
                for user_skill in user_skills
            ],
        )
    )


@router.put("/me", response_model=schemas.User)
async def update_me(
    schema: schemas.UserCRUD,
    user: models.User = Depends(dependencies.get_user),
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    for field, value in schema:
        setattr(user, field, value)

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return schemas.User.model_validate(user)


@router.get("/me/createdProjects", response_model=list[schemas.Project])
async def get_created_projects(
    user: models.User = Depends(dependencies.get_user),
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    project_result = await session.exec(select(models.Project).where(models.Project.creator_id == user.id))  # noqa
    projects = project_result.all()

    return list(map(schemas.Project.model_validate, projects))


@router.post("/me/createdProjects", response_model=schemas.Project)
async def create_created_project(
    schema: schemas.ProjectCRUD,
    user: models.User = Depends(dependencies.get_user),
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    project = models.Project(
        **schema.model_dump(),
        creator_id=user.id,
    )
    session.add(project)
    await session.commit()
    await session.refresh(project)

    return schemas.Project.model_validate(project)


@router.get("/me/createdProjects/{project_id}/members", response_model=list[schemas.UserMember])
async def get_created_project_members(
    created_project: tp.Annotated[models.Project, Depends(dependencies.get_created_project)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    users_result = await session.exec(
        select(models.User, models.ProjectUser.role)  # noqa
        .join(models.ProjectUser)
        .where(models.ProjectUser.project_id == created_project.id)  # noqa
    )
    users = users_result.all()

    return [schemas.UserMember.model_validate(dict(**user.model_dump(), role=role)) for user, role in users]


@router.get("/me/createdProjects/{project_id}/tasks", response_model=list[schemas.Task])
async def get_created_project_tasks(
    created_project: tp.Annotated[models.Project, Depends(dependencies.get_created_project)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    task_result = await session.exec(select(models.Task).where(models.Task.project_id == created_project.id))  # noqa
    tasks = task_result.all()

    return list(map(schemas.Task.model_validate, tasks))


@router.post("/me/createdProjects/{project_id}/tasks", response_model=schemas.Task)
async def create_created_project_task(
    schema: schemas.TaskCRUD,
    created_project: tp.Annotated[models.Project, Depends(dependencies.get_created_project)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    task = models.Task(
        **schema.model_dump(),
        project_id=created_project.id,
        status="New"
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)

    return schemas.Task.model_validate(task)


@router.put("/me/createdProjects/{project_id}/tasks/{task_id}", response_model=schemas.Task)
async def update_created_project_task(
    schema: schemas.TaskCRUD,
    created_project: tp.Annotated[models.Project, Depends(dependencies.get_created_project)],
    task: tp.Annotated[models.Task, Depends(dependencies.get_project_task)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    for field, value in schema:
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return schemas.Task.model_validate(task)


@router.delete("/me/createdProjects/{project_id}/tasks/{task_id}", response_model=str)
async def delete_created_project_task(
    created_project: tp.Annotated[models.Project, Depends(dependencies.get_created_project)],
    task: tp.Annotated[models.Task, Depends(dependencies.get_project_task)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    await session.delete(task)
    await session.commit()

    return "OK"


@router.get("/me/memberProjects", response_model=list[schemas.Project])
async def get_member_projects(
    user: models.User = Depends(dependencies.get_user),
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    project_result = await session.exec(
        select(models.Project)
        .join(models.ProjectUser)
        .where(models.ProjectUser.user_id == user.id)  # noqa
    )
    projects = project_result.all()

    return list(map(schemas.Project.model_validate, projects))


@router.get("/me/memberProjects/{project_id}/tasks", response_model=list[schemas.Task])
async def get_member_project_tasks(
    member_project: tp.Annotated[models.Project, Depends(dependencies.get_member_project)],
    user: models.User = Depends(dependencies.get_user),
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    task_result = await session.exec(
        select(models.Task)
        .join(models.Project)
        .where(models.Task.project_id == member_project.id)  # noqa
        .join(models.User)
        .where(models.Task.assignee_id == user.id)  # noqa
    )
    tasks = task_result.all()

    return list(map(schemas.Task.model_validate, tasks))


@router.put("/me/memberProjects/{project_id}/tasks/{task_id}", response_model=schemas.Task)
async def update_member_project_task(
    schema: schemas.TaskStatusCRUD,
    member_project: tp.Annotated[models.Project, Depends(dependencies.get_member_project)],
    task: tp.Annotated[models.Task, Depends(dependencies.get_project_task)],
    session: dependencies.AsyncSession = Depends(dependencies.get_session),
):
    for field, value in schema:
        setattr(task, field, value)

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return schemas.Task.model_validate(task)
