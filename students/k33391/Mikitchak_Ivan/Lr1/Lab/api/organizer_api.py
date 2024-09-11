from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlmodel import Session

from typing import List, Optional

from dependencies import oauth2_scheme
from connection import get_session
from utilities import get_user_by_token
from models import (
    Contest,
    JoinAsOrganizerForm,
    Organizer,
    OrganizerRole,
    OrganizerSerialized,
    UserSerialized,
)


router = APIRouter()


# Create an organizer (join contest as an organizer)
@router.post("/contests/{contest_id}/organizers", status_code=status.HTTP_201_CREATED)
def create_organizer(contest_id: int,
                     request: JoinAsOrganizerForm,
                     token: Optional[str] = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> OrganizerSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    print(contest)
    if contest.code != request.code:
        raise HTTPException(status_code=400, detail="Incorrect code.")
    
    current_organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                                (Organizer.contest_id == contest_id))).scalar_one_or_none()
    if current_organizer is not None:
        raise HTTPException(status_code=409, detail=f"User is already an organizer of this contest with id {current_organizer.id}.")    
    
    organizer = Organizer(user=user, contest=contest, role=OrganizerRole.moderator)
    
    session.add(organizer)
    session.commit()
    session.refresh(organizer)
    
    return OrganizerSerialized(id=organizer.id,
                               user=UserSerialized(id=organizer.user_id,
                                                   email=organizer.user.email,
                                                   first_name=organizer.user.first_name,
                                                   last_name=organizer.user.last_name),
                               role=organizer.role)


# Read organizers (search)
@router.get("/contests/{contest_id}/organizers")
def read_organizers(contest_id: int,
                    token: Optional[str] = Depends(oauth2_scheme),
                    session: Session = Depends(get_session)) -> List[OrganizerSerialized]:
    get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizers = session.exec(select(Organizer).where(Organizer.contest_id == contest_id)).all()
    
    return [OrganizerSerialized(id=organizer_tuple[0].id,
                                user=UserSerialized(id=organizer_tuple[0].user_id,
                                                    email=organizer_tuple[0].user.email,
                                                    first_name=organizer_tuple[0].user.first_name,
                                                    last_name=organizer_tuple[0].user.last_name),
                                role=organizer_tuple[0].role) for organizer_tuple in organizers]


# Read my organizer
@router.get("/contests/{contest_id}/organizers/me")
def read_my_organizer(contest_id: int,
                      token: Optional[str] = Depends(oauth2_scheme),
                      session: Session = Depends(get_session)) -> OrganizerSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.user_id == user.id))).scalar_one_or_none()
    if organizer is None:
        raise HTTPException(status_code=404, detail="You are not an organizer of this contest.")
    
    return OrganizerSerialized(id=organizer.id,
                               user=UserSerialized(id=organizer.user_id,
                                                   email=organizer.user.email,
                                                   first_name=organizer.user.first_name,
                                                   last_name=organizer.user.last_name),
                               role=organizer.role)


# Delete my organizer (leave contest as an organizer)
@router.delete("/contests/{contest_id}/organizers/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_organizer(contest_id: int,
                        token: Optional[str] = Depends(oauth2_scheme),
                        session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.user_id == user.id))).scalar_one_or_none()
    if organizer is None:
        raise HTTPException(status_code=404, detail="You are not an organizer of this contest.")
    
    session.delete(organizer)
    session.commit()


# Read an organizer
@router.get("/contests/{contest_id}/organizers/{organizer_id}")
def read_organizer(contest_id: int,
                   organizer_id: int,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> OrganizerSerialized:
    get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
      
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.id == organizer_id))).scalar_one_or_none()
    if organizer is None:
        raise HTTPException(status_code=404, detail="Organizer not found.")
    
    return OrganizerSerialized(id=organizer.id,
                               user=UserSerialized(id=organizer.user_id,
                                                   email=organizer.user.email,
                                                   first_name=organizer.user.first_name,
                                                   last_name=organizer.user.last_name),
                               role=organizer.role)


# Delete an organizer (kick)
@router.delete("/contests/{contest_id}/organizers/{organizer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organizer(contest_id: int,
                     organizer_id: int,
                     token: Optional[str] = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)):
    get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.id == organizer_id))).scalar_one_or_none()
    if organizer is None:
        raise HTTPException(status_code=404, detail="Organizer not found.")
    
    session.delete(organizer)
    session.commit()
