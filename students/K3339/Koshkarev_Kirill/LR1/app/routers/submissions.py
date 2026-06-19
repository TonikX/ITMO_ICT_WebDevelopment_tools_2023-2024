"""API работ и их оценки (загрузка прототипов + оценка судьями).

Оценка — ассоциативная сущность Evaluation со связью many-to-many
Submission <-> User(судья) и характеризующими полями score, comment.
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models import Evaluation, Submission, Task, Team, TeamMember, User, UserRole
from app.schemas import (
    EvaluationCreate,
    EvaluationOut,
    SubmissionCreate,
    SubmissionDetailOut,
    SubmissionOut,
)

router = APIRouter(prefix="/submissions", tags=["Работы и оценки"])


@router.post("", response_model=SubmissionOut, status_code=status.HTTP_201_CREATED)
def create_submission(
    data: SubmissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Загрузка работы командой. Загрузить может только участник команды."""
    team = db.query(Team).filter(Team.id == data.team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

    task = db.query(Task).filter(Task.id == data.task_id).first()
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

    is_member = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == data.team_id, TeamMember.user_id == current_user.id)
        .first()
    )
    if is_member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Загружать работу может только участник команды",
        )

    submission = Submission(
        team_id=data.team_id,
        task_id=data.task_id,
        title=data.title,
        description=data.description,
        repo_url=data.repo_url,
    )
    db.add(submission)
    db.commit()
    db.refresh(submission)
    return submission


@router.get("", response_model=List[SubmissionOut])
def list_submissions(db: Session = Depends(get_db)):
    return db.query(Submission).all()


@router.get("/{submission_id}", response_model=SubmissionDetailOut)
def get_submission(submission_id: int, db: Session = Depends(get_db)):
    """Работа вместе со всеми оценками судей."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работа не найдена")
    return submission


@router.post(
    "/{submission_id}/evaluate",
    response_model=EvaluationOut,
    status_code=status.HTTP_201_CREATED,
)
def evaluate_submission(
    submission_id: int,
    data: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.judge)),
):
    """Оценить работу (только судья). Один судья оценивает работу один раз."""
    submission = db.query(Submission).filter(Submission.id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Работа не найдена")

    if data.score > submission.task.max_score:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Оценка превышает максимально допустимую для задачи",
        )

    evaluation = Evaluation(
        submission_id=submission_id,
        judge_id=current_user.id,
        score=data.score,
        comment=data.comment,
    )
    db.add(evaluation)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Вы уже оценивали эту работу",
        )
    db.refresh(evaluation)
    return evaluation
