from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from schemas import Submission, SubmissionDefault
from database import get_session
from typing_extensions import TypedDict

router = APIRouter(tags=["Submissions"])

@router.post("/submission-create", status_code=status.HTTP_201_CREATED)
def submission_create(submission: SubmissionDefault, session=Depends(get_session)) -> Submission:
    submission = Submission.model_validate(submission)
    session.add(submission)
    session.commit()
    session.refresh(submission)
    return submission


@router.get("/list-submissions", status_code=status.HTTP_200_OK)
def submissions_list(session=Depends(get_session)) -> list[Submission]:
    return session.query(Submission).all()


@router.get("/submission/{submission_id}", status_code=status.HTTP_200_OK)
def submission_get(submission_id: int, session=Depends(get_session)) -> Submission:
    obj = session.get(Submission, submission_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="submission not found")
    return obj


@router.patch("/submission/update/{submission_id}", status_code=status.HTTP_202_ACCEPTED)
def submission_update(submission_id: int, submission: SubmissionDefault, session=Depends(get_session)) \
        -> Submission:
    db_submission = session.get(Submission, submission_id)
    if not db_submission:
        raise HTTPException(status_code=404, detail="submission not found")

    submission_data = submission.model_dump(exclude_unset=True)
    for key, value in submission_data.items():
        setattr(db_submission, key, value)
    session.add(db_submission)
    session.commit()
    session.refresh(db_submission)
    return db_submission


@router.delete("/submission/delete/{submission_id}", status_code=status.HTTP_204_NO_CONTENT)
def submission_delete(submission_id: int, session=Depends(get_session)):
    submission = session.get(Submission, submission_id)
    if not submission:
        raise HTTPException(status_code=404, detail="submission not found")
    session.delete(submission)
    session.commit()
    return {"ok": True}

