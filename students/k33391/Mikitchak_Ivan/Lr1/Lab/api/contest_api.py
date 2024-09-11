from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select

from typing import Optional, List

from connection import get_session
from dependencies import oauth2_scheme
from models import (
    Contest,
    ContestSerializedAdmin,
    ContestCreateForm,
    ContestSerialized,
    ContestUpdateForm,
    OrganizerRole,
    Organizer)
from utilities import get_user_by_token, generate_code

from datetime import datetime


router = APIRouter()


# Create a contest
@router.post("/contests", status_code=status.HTTP_201_CREATED)
def create_contest(request: ContestCreateForm,
                   token: str = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> ContestSerializedAdmin:
    user = get_user_by_token(token, session)
    
    code = generate_code()
    contest = Contest(title=request.title,
                      code=code,
                      description=request.description,
                      start_date=request.start_date,
                      end_date=request.end_date)
    
    print(request.start_date, request.end_date)
    print(contest.start_date, contest.end_date)
    
    session.add(contest)
    session.commit()
    session.refresh(contest)
    
    print(contest.start_date, contest.end_date)
    
    organizer = Organizer(user=user, contest=contest, role=OrganizerRole.admin)
    
    session.add(organizer)
    session.commit()
    session.refresh(organizer)
    
    return ContestSerializedAdmin(id=contest.id,
                           title=contest.title,
                           code=contest.code,
                           description=contest.description,
                           start_date=contest.start_date,
                           end_date=contest.end_date)


# Read contests (search)
@router.get("/contests")
def read_contests(keywords: Optional[str] = None,
                  offset: int = Query(0, ge=0),
                  limit: int = Query(10, gt=0, le=100),
                  token: Optional[str] = Depends(oauth2_scheme),
                  session: Session = Depends(get_session)) -> List[ContestSerialized]:
    get_user_by_token(token, session)
    
    query = select(Contest)    
    if keywords is not None:
        query = query.where((Contest.title.ilike(f"%{keywords}%")) |
                            (Contest.description.ilike(f"%{keywords}%")))
    
    contests = session.exec(query.offset(offset).limit(limit)).all()
    
    return [ContestSerialized(id=contest.id,
                              title=contest.title,
                              description=contest.description,
                              start_date = contest.start_date,
                              end_date = contest.end_date) for contest in contests]


# Read a contest
@router.get("/contests/{contest_id}")
def read_contest(contest_id: int,
                     token: Optional[str] = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> ContestSerializedAdmin | ContestSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest.id))).one_or_none()
    
    if organizer is not None and organizer.role == OrganizerRole.admin:
        return ContestSerializedAdmin(id=contest.id,
                                      title=contest.title,
                                      code=contest.code,
                                      description=contest.description,
                                      start_date=contest.start_date,
                                      end_date=contest.end_date)
    else:
        return ContestSerialized(id=contest.id,
                                 title=contest.title,
                                 description=contest.description,
                                 start_date=contest.start_date,
                                 end_date=contest.end_date)


# Update contest code
@router.post("/contests/{contest_id}/update_code")
def update_contest_code(contest_id: int,
                        token: Optional[str] = Depends(oauth2_scheme),
                        session: Session = Depends(get_session)) -> ContestSerializedAdmin:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest.id))).one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="You are not an organizer of this contest.")
    if organizer.role != OrganizerRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can update contest code.")
    
    contest.code = generate_code()
    
    session.add(contest)
    session.commit()
    session.refresh(contest)
    
    return ContestSerializedAdmin(id=contest.id,
                                title=contest.title,
                                code=contest.code,
                                description=contest.description,
                                start_date=contest.start_date,
                                end_date=contest.end_date)


# Update a contest (all fields except code)
@router.put("/contests/{contest_id}")
def update_contest(contest_id: int,
                   request: ContestUpdateForm,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> ContestSerializedAdmin | ContestSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest.id))).one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="You are not an organizer of this contest.")
    
    if request.title is not None:
        contest.title = request.title
    if request.description is not None:
        contest.description = request.description
    if request.start_date is not None:
        contest.start_date = request.start_date
    if request.end_date is not None:
        contest.end_date = request.end_date
    
    session.add(contest)
    session.commit()
    session.refresh(contest)
    
    if organizer.role == OrganizerRole.admin:
        return ContestSerializedAdmin(id=contest.id,
                                      title=contest.title,
                                      code=contest.code,
                                      description=contest.description,
                                      start_date=contest.start_date,
                                      end_date=contest.end_date)
    else:
        return ContestSerialized(id=contest.id,
                                 title=contest.title,
                                 description=contest.description,
                                 start_date=contest.start_date,
                                 end_date=contest.end_date)


# Delete a contest
@router.delete("/contests/{contest_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contest(contest_id: int,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest.id))).one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="You are not an organizer of this contest.")
    if organizer.role != OrganizerRole.admin:
        raise HTTPException(status_code=403, detail="Only admins can delete their contest.")
    
    session.delete(contest)
    session.commit()
