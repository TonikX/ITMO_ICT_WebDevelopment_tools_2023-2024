from fastapi import Response, APIRouter
from sqlalchemy import select, exc

from lab1.prac2.db.database import DatabaseSession
from lab1.prac2.db.models import Sprint as SprintModel
from lab1.prac2.rest.sprint.schemas import (
    SprintResponse,
    NotFoundDataResponse,
    SprintDataResponse,
    SprintBodySchema,
    MessageResponse,
)

router = APIRouter(prefix="/sprints", tags=["sprints"])


@router.get("/")
def get_sprints(session: DatabaseSession) -> list[SprintResponse]:
    stmt = select(SprintModel).order_by(SprintModel.id)
    sprint_models = session.scalars(stmt).all()
    return [SprintResponse.model_validate(sprint_model) for sprint_model in sprint_models]


@router.get("/{sprint_id}", responses={200: {"model": SprintDataResponse}, 404: {"model": NotFoundDataResponse}})
def get_sprint(sprint_id: int, session: DatabaseSession, response: Response):
    stmt = select(SprintModel).where(SprintModel.id == sprint_id)
    try:
        sprint_model = session.scalars(stmt).one()
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Sprint not found")

    return SprintDataResponse(status=200, data=SprintResponse.model_validate(sprint_model))


@router.post("/")
def add_sprint(sprint_body: SprintBodySchema, session: DatabaseSession) -> SprintDataResponse:
    sprint_model = SprintModel(
        title=sprint_body.title,
        start_at=sprint_body.start_at,
        end_at=sprint_body.end_at,
    )
    session.add(sprint_model)
    session.commit()
    session.refresh(sprint_model)

    return SprintDataResponse(status=200, data=SprintResponse.model_validate(sprint_model))


@router.delete("/{sprint_id}", status_code=201)
def delete_sprint(sprint_id: int, session: DatabaseSession, response: Response) -> MessageResponse:
    stmt = select(SprintModel).where(SprintModel.id == sprint_id)
    try:
        sprint_model = session.scalars(stmt).one()
    except exc.NoResultFound:
        response.status_code = 404
        return MessageResponse(status=404, message="Task not found")

    session.delete(sprint_model)
    session.commit()

    return MessageResponse(status=201, message="deleted")


@router.patch("/{sprint_id}", responses={200: {"model": SprintDataResponse}, 404: {"model": NotFoundDataResponse}})
def update_sprint(sprint_id: int, sprint_body: SprintBodySchema, session: DatabaseSession, response: Response):
    stmt = select(SprintModel).where(SprintModel.id == sprint_id)
    try:
        sprint_model = session.scalars(stmt).one()
    except exc.NoResultFound:
        response.status_code = 404
        return NotFoundDataResponse(status=404, data="Task not found")

    for key, value in sprint_body.model_dump().items():
        setattr(sprint_model, key, value)

    session.add(sprint_model)
    session.commit()
    session.refresh(sprint_model)

    return SprintDataResponse(status=200, data=SprintResponse.model_validate(sprint_model))


