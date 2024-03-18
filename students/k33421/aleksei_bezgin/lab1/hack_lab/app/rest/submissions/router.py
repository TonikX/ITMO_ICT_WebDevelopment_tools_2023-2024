from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.db.models import Submission as SubmissionModel
from app.rest.dependencies import DatabaseSession
from app.rest.submissions.schemas import Submission, SubmissionCreateData, SubmissionUpdateData

router = APIRouter()


@router.get("/")
def get_submissions(session: DatabaseSession) -> list[Submission]:
    stmt = select(SubmissionModel)
    return session.scalars(stmt).all()


@router.get("/{submission_id}")
def get_submission(submission_id: int, session: DatabaseSession) -> Submission:
    stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
    return session.scalars(stmt).first()


@router.post("/")
def create_submission(submission_data: SubmissionCreateData, session: DatabaseSession) -> Submission:
    submission_model = SubmissionModel.model_validate(submission_data)
    session.add(submission_model)
    session.commit()
    session.refresh(submission_model)

    return submission_model


@router.patch("/{submission_id}")
def update_submission(
    submission_id: int, submission_data: SubmissionUpdateData, session: DatabaseSession
) -> Submission:
    submission_stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
    submission_model = session.scalars(submission_stmt).first()
    if not submission_model:
        raise HTTPException(status_code=404, detail="Submission not found")

    for key, value in submission_data.model_dump(exclude_unset=True).items():
        setattr(submission_model, key, value)

    session.add(submission_model)
    session.commit()
    session.refresh(submission_model)

    return submission_model


@router.delete("/{submission_id}")
def delete_submission(submission_id: int, session: DatabaseSession) -> str:
    submission_stmt = select(SubmissionModel).where(SubmissionModel.id == submission_id)
    submission_model = session.scalars(submission_stmt).first()
    if not submission_model:
        raise HTTPException(status_code=404, detail="Submission not found")

    team = submission_model.team
    task = submission_model.task

    session.delete(submission_model)
    session.commit()

    return f"Submission of {team.name} for task {task.title} deleted"