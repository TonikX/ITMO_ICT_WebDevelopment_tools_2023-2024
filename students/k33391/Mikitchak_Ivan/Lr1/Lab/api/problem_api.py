from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from typing import List, Optional

from dependencies import oauth2_scheme
from connection import get_session
from utilities import get_user_by_token
from models import (
    Contest,
    CreateProblemForm,
    Organizer,
    Participant,
    Problem,
    ProblemSerialized,
    ProblemSerializedShort,
    UpdateProblemForm,
)

from datetime import datetime


router = APIRouter()


# Create a problem
@router.post("/contests/{contest_id}/problems", status_code=status.HTTP_201_CREATED)
def create_problem(contest_id: int,
                   request: CreateProblemForm,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> ProblemSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest_id))).one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="User is not an organizer of this contest.")
    
    problem = Problem(contest=contest, title=request.title, description=request.description)
    
    session.add(problem)
    session.commit()
    session.refresh(problem)
    
    return ProblemSerialized(id=problem.id, title=problem.title, description=problem.description)


# Read problems (search)
@router.get("/contests/{contest_id}/problems")
def read_problems(contest_id: int,
                  token: Optional[str] = Depends(oauth2_scheme),
                  session: Session = Depends(get_session)) -> List[ProblemSerializedShort]:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")

    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.user_id == user.id))).one_or_none()
    if organizer is None and participant is None:
        raise HTTPException(status_code=403, detail="User is neither participant nor organizer of this contest.")
    
    problems = session.exec(select(Problem).where(Problem.contest_id == contest_id)).all()
    
    if organizer is None and datetime.now().astimezone() < contest.start_date:
        raise HTTPException(status_code=403, detail="Can't access contest problems before the start of the contest.")
    
    return [ProblemSerializedShort(id=problem.id, title=problem.title) for problem in problems]


# Read a problem
@router.get("/contests/{contest_id}/problems/{problem_id}")
def read_problem(contest_id: int,
                 problem_id: int,
                 token: Optional[str] = Depends(oauth2_scheme),
                 session: Session = Depends(get_session)) -> ProblemSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")

    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.user_id == user.id))).one_or_none()
    if organizer is None and participant is None:
        raise HTTPException(status_code=403, detail="User is neither participant nor organizer of this contest.")
    
    problem = session.exec(select(Problem).where((Problem.contest_id == contest_id) &
                                                 (Problem.id == problem_id))).one_or_none()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    
    if organizer is None and datetime.now().astimezone() < contest.start_date:
        raise HTTPException(status_code=403, detail="Can't access contest problems before the start of the contest.")
    
    return ProblemSerialized(id=problem.id, title=problem.title, description=problem.description)


# Update a problem
@router.put("/contests/{contest_id}/problems/{problem_id}")
def update_problem(contest_id: int,
                   problem_id: int,
                   request: UpdateProblemForm,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> ProblemSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    problem = session.exec(select(Problem).where((Problem.contest_id == contest_id) &
                                                 (Problem.id == problem_id))).one_or_none()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest_id))).one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="User is not an organizer of this contest.")
    
    if request.title is not None:
        problem.title = request.title
    if request.description is not None:
        problem.description = request.description
    
    session.add(problem)
    session.commit()
    session.refresh(problem)
    
    return ProblemSerialized(id=problem.id, title=problem.title, description=problem.description)


# Delete a problem
@router.delete("/contests/{contest_id}/problems/{problem_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_problem(contest_id: int,
                   problem_id: int,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    problem = session.exec(select(Problem).where((Problem.contest_id == contest_id) &
                                                 (Problem.id == problem_id))).one_or_none()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest_id))).one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="User is not an organizer of this contest.")
    
    session.delete(problem)
    session.commit()
