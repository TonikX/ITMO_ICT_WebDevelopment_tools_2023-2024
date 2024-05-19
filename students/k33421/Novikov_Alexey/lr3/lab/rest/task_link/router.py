from fastapi import Response, APIRouter
from sqlalchemy import select, exc, insert, delete, update
from sqlalchemy.orm import contains_eager, aliased

from db.database import DatabaseSession
from db.models import Task as TaskModel, TaskLink as TaskLinkModel, Sprint as SprintModel
from rest.task_link.schemas import (
    NotFoundDataResponse,
    TaskLinkBodySchema,
    TaskLinkResponse,
    TaskLinkDataResponse,
    MessageResponse,
    TaskLinkUpdateSchema,
)

router = APIRouter(prefix="/task_links", tags=["task_links"])


@router.get("/")
def get_task_links(session: DatabaseSession) -> list[TaskLinkResponse]:
    parent_task = aliased(TaskModel, name="parent_task")
    parent_sprint = aliased(SprintModel, name="parent_sprint")
    child_task = aliased(TaskModel, name="child_task")
    child_sprint = aliased(SprintModel, name="child_sprint")

    stmt = (
        select(TaskLinkModel)
        .join(parent_task, onclause=TaskLinkModel.parent_task_id == parent_task.id)
        .join(parent_sprint, onclause=parent_task.sprint_id == parent_sprint.id, isouter=True)
        .join(child_task, onclause=TaskLinkModel.child_task_id == child_task.id)
        .join(child_sprint, onclause=child_task.sprint_id == child_sprint.id, isouter=True)
        .options(
            contains_eager(TaskLinkModel.parent_task.of_type(parent_task)).contains_eager(parent_task.sprint),
            contains_eager(TaskLinkModel.child_task.of_type(child_task)).contains_eager(child_task.sprint),
        )
    )
    task_link_models = session.scalars(stmt).unique().all()
    return [TaskLinkResponse.model_validate(task_link_model) for task_link_model in task_link_models]


@router.get(
    "/{child_task_id}/{parent_task_id}",
    responses={200: {"model": TaskLinkDataResponse}, 404: {"model": NotFoundDataResponse}},
)
def get_task_links(child_task_id: int, parent_task_id: int, session: DatabaseSession, response: Response):
    parent_task = aliased(TaskModel, name="parent_task")
    parent_sprint = aliased(SprintModel, name="parent_sprint")
    child_task = aliased(TaskModel, name="child_task")
    child_sprint = aliased(SprintModel, name="child_sprint")

    stmt = (
        select(TaskLinkModel)
        .join(parent_task, onclause=TaskLinkModel.parent_task_id == parent_task.id)
        .join(parent_sprint, onclause=parent_task.sprint_id == parent_sprint.id, isouter=True)
        .join(child_task, onclause=TaskLinkModel.child_task_id == child_task.id)
        .join(child_sprint, onclause=child_task.sprint_id == child_sprint.id, isouter=True)
        .options(
            contains_eager(TaskLinkModel.parent_task.of_type(parent_task)).contains_eager(parent_task.sprint),
            contains_eager(TaskLinkModel.child_task.of_type(child_task)).contains_eager(child_task.sprint),
        )
        .where(child_task.id == child_task_id, parent_task.id == parent_task_id)
    )
    try:
        task_link_model = session.scalars(stmt).unique().one()
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    return TaskLinkDataResponse(status=200, data=TaskLinkResponse.model_validate(task_link_model))


@router.post("/", responses={200: {"model": TaskLinkDataResponse}, 404: {"model": NotFoundDataResponse}})
def add_task_link(task_link_body: TaskLinkBodySchema, session: DatabaseSession, response: Response):
    parent_task = aliased(TaskModel, name="parent_task")
    parent_sprint = aliased(SprintModel, name="parent_sprint")
    child_task = aliased(TaskModel, name="child_task")
    child_sprint = aliased(SprintModel, name="child_sprint")

    insert_cte = (
        insert(TaskLinkModel)
        .values(
            parent_task_id=task_link_body.parent_task_id,
            child_task_id=task_link_body.child_task_id,
            status=task_link_body.status,
        )
        .returning(TaskLinkModel)
        .cte("task_link")
    )
    stmt = (
        select(TaskLinkModel)
        .from_statement(
            select(insert_cte.columns, parent_task, child_task, parent_sprint, child_sprint)
            .join(parent_task, onclause=insert_cte.c.parent_task_id == parent_task.id)
            .join(parent_sprint, onclause=parent_task.sprint_id == parent_sprint.id, isouter=True)
            .join(child_task, onclause=insert_cte.c.child_task_id == child_task.id)
            .join(child_sprint, onclause=child_task.sprint_id == child_sprint.id, isouter=True)
        )
        .options(
            contains_eager(TaskLinkModel.parent_task.of_type(parent_task)).contains_eager(parent_task.sprint),
            contains_eager(TaskLinkModel.child_task.of_type(child_task)).contains_eager(child_task.sprint),
        )
    )

    try:
        task_link_model = session.scalars(stmt).one()
    except exc.IntegrityError:
        response.status_code = 400
        return NotFoundDataResponse(status=400, data="Task link already exists")
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    task_link_response = TaskLinkResponse.model_validate(task_link_model)

    session.commit()

    return TaskLinkDataResponse(status=200, data=task_link_response)


@router.delete("/{child_task_id}/{parent_task_id}", status_code=201)
def delete_task_link(
    child_task_id: int, parent_task_id: int, session: DatabaseSession, response: Response
) -> MessageResponse:
    stmt = delete(TaskLinkModel).where(
        TaskLinkModel.child_task_id == child_task_id, TaskLinkModel.parent_task_id == parent_task_id
    )
    result = session.execute(stmt)

    if result.rowcount == 0:
        response.status_code = 404
        return MessageResponse(status=404, message="Task not found")

    session.commit()

    return MessageResponse(status=201, message="deleted")


@router.patch(
    "/{child_task_id}/{parent_task_id}",
    responses={200: {"model": TaskLinkDataResponse}, 404: {"model": NotFoundDataResponse}},
)
def update_task_link(
    child_task_id: int,
    parent_task_id: int,
    task_link_body: TaskLinkUpdateSchema,
    session: DatabaseSession,
    response: Response,
):
    parent_task = aliased(TaskModel, name="parent_task")
    parent_sprint = aliased(SprintModel, name="parent_sprint")
    child_task = aliased(TaskModel, name="child_task")
    child_sprint = aliased(SprintModel, name="child_sprint")

    update_cte = (
        update(TaskLinkModel)
        .where(TaskLinkModel.child_task_id == child_task_id, TaskLinkModel.parent_task_id == parent_task_id)
        .values(status=task_link_body.status)
        .returning(TaskLinkModel)
        .cte("task_link")
    )
    stmt = (
        select(TaskLinkModel)
        .from_statement(
            select(update_cte.columns, parent_task, child_task, parent_sprint, child_sprint)
            .join(parent_task, onclause=update_cte.c.parent_task_id == parent_task.id)
            .join(parent_sprint, onclause=parent_task.sprint_id == parent_sprint.id, isouter=True)
            .join(child_task, onclause=update_cte.c.child_task_id == child_task.id)
            .join(child_sprint, onclause=child_task.sprint_id == child_sprint.id, isouter=True)
        )
        .options(
            contains_eager(TaskLinkModel.parent_task.of_type(parent_task)).contains_eager(parent_task.sprint),
            contains_eager(TaskLinkModel.child_task.of_type(child_task)).contains_eager(child_task.sprint),
        )
    )

    try:
        task_link_model = session.scalars(stmt).one()
    except exc.IntegrityError:
        response.status_code = 400
        return NotFoundDataResponse(status=400, data="Task link already exists")
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    task_link_response = TaskLinkResponse.model_validate(task_link_model)

    session.commit()

    return TaskLinkDataResponse(status=200, data=task_link_response)
