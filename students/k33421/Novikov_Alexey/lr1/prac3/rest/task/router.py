from fastapi import Response, APIRouter
from sqlalchemy import select, exc, insert, delete, update
from sqlalchemy.orm import contains_eager, aliased

from ...db.database import DatabaseSession
from ...db.models import Task as TaskModel, TaskLink as TaskLinkModel, Sprint as SprintModel
from ...rest.task.schemas import (
    TaskResponse,
    TaskBodySchema,
    MessageResponse,
    NotFoundDataResponse,
    TaskDataResponse,
    TaskWithLinksResponse,
    TaskWithLinksDataResponse,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
def get_tasks(session: DatabaseSession) -> list[TaskWithLinksResponse]:
    stmt = (
        select(TaskModel)
        .join(SprintModel, isouter=True)
        .join(TaskLinkModel, onclause=TaskModel.id == TaskLinkModel.parent_task_id, isouter=True)
        .join(aliased(TaskModel, name="child"), onclause=TaskLinkModel.child_task_id == TaskModel.id, isouter=True)
        .options(
            contains_eager(TaskModel.sprint),
            contains_eager(TaskModel.linked_tasks).contains_eager(TaskLinkModel.child_task),
        )
        .order_by(TaskModel.id)
    )
    task_models = session.scalars(stmt).unique().all()
    return [TaskWithLinksResponse.model_validate(task_model) for task_model in task_models]


@router.get("/{task_id}", responses={200: {"model": TaskWithLinksDataResponse}, 404: {"model": NotFoundDataResponse}})
def get_task(task_id: int, session: DatabaseSession, response: Response):
    stmt = (
        select(TaskModel)
        .join(SprintModel, isouter=True)
        .join(TaskLinkModel, onclause=TaskModel.id == TaskLinkModel.parent_task_id, isouter=True)
        .join(aliased(TaskModel, name="child"), onclause=TaskLinkModel.child_task_id == TaskModel.id, isouter=True)
        .options(
            contains_eager(TaskModel.sprint),
            contains_eager(TaskModel.linked_tasks).contains_eager(TaskLinkModel.child_task),
        )
        .where(TaskModel.id == task_id)
    )
    try:
        task_model = session.scalars(stmt).unique().one()
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    return TaskWithLinksDataResponse(status=200, data=TaskWithLinksResponse.model_validate(task_model))


@router.post("/", responses={200: {"model": TaskDataResponse}, 404: {"model": NotFoundDataResponse}})
def add_task(task_body: TaskBodySchema, session: DatabaseSession, response: Response):
    insert_cte = (
        insert(TaskModel)
        .values(
            summary=task_body.summary,
            priority=task_body.priority,
            description=task_body.description,
            planned_end_at=task_body.planned_end_at,
            status=task_body.status,
            sprint_id=task_body.sprint_id,
        )
        .returning(TaskModel)
        .cte("task")
    )
    stmt = (
        select(TaskModel)
        .from_statement(
            select(insert_cte.columns, SprintModel).join(
                SprintModel, onclause=insert_cte.c.sprint_id == SprintModel.id, isouter=True
            )
        )
        .options(contains_eager(TaskModel.sprint))
    )
    try:
        task_model = session.scalars(stmt).one()
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    return TaskDataResponse(status=200, data=TaskResponse.model_validate(task_model))


@router.delete("/{task_id}", status_code=201)
def delete_task(task_id: int, session: DatabaseSession, response: Response) -> MessageResponse:
    stmt = delete(TaskModel).where(TaskModel.id == task_id)
    result = session.execute(stmt)

    if result.rowcount == 0:
        response.status_code = 404
        return MessageResponse(status=404, message="Task not found")

    session.commit()

    return MessageResponse(status=201, message="deleted")


@router.patch("/{task_id}", responses={200: {"model": TaskWithLinksDataResponse}, 404: {"model": NotFoundDataResponse}})
def update_task(task_id: int, task_body: TaskBodySchema, session: DatabaseSession, response: Response):
    child = aliased(TaskModel, name="child")
    child_sprint = aliased(SprintModel, name="child_sprint")
    update_cte = (
        update(TaskModel)
        .where(TaskModel.id == task_id)
        .values(
            summary=task_body.summary,
            priority=task_body.priority,
            description=task_body.description,
            planned_end_at=task_body.planned_end_at,
            status=task_body.status,
            sprint_id=task_body.sprint_id,
        )
        .returning(TaskModel)
        .cte("task")
    )
    stmt = (
        select(TaskModel)
        .from_statement(
            select(update_cte.columns, SprintModel, TaskLinkModel, child, child_sprint)
            .join(SprintModel, onclause=update_cte.c.sprint_id == SprintModel.id, isouter=True)
            .join(TaskLinkModel, onclause=update_cte.c.id == TaskLinkModel.parent_task_id, isouter=True)
            .join(child, onclause=TaskLinkModel.child_task_id == TaskModel.id, isouter=True)
            .join(child_sprint, onclause=child.sprint_id == SprintModel.id, isouter=True)
        )
        .options(
            contains_eager(TaskModel.sprint),
            contains_eager(TaskModel.linked_tasks).contains_eager(TaskLinkModel.child_task),
        )
    )

    try:
        task_model = session.scalars(stmt).one()
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    task_response = TaskWithLinksResponse.model_validate(task_model)

    session.commit()

    return TaskWithLinksDataResponse(status=200, data=task_response)
