from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlmodel import Session

from typing import List, Optional

from dependencies import oauth2_scheme
from connection import get_session
from utilities import get_user_by_token
from models import (
    Contest,
    Organizer,
    Participant,
    ParticipantSerialized,
    ScoreParticipantForm,
    TeamMember,
    User,
    UserSerialized,
)

router = APIRouter()

    
# Create a participant (sign up for a contest)
@router.post("/contests/{contest_id}/participants", status_code=status.HTTP_201_CREATED)
def create_participant(contest_id: int,
                       token: Optional[str] = Depends(oauth2_scheme),
                       session: Session = Depends(get_session)) -> ParticipantSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    if contest.start_date <= datetime.now().astimezone():
        raise HTTPException(status_code=403, detail="Can't sign up for contest after it has started.")
    
    current_participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                                 (Participant.contest_id == contest_id))).scalar_one_or_none()
    if current_participant is not None:
        raise HTTPException(status_code=409, detail=f"User is already signed up for this contest with participant_id {current_participant.id}")
    
    participant = Participant(user_id=user.id, contest_id=contest.id)
    
    session.add(participant)
    session.commit()
    session.refresh(participant)
    
    return ParticipantSerialized(id=participant.id,
                                 user=UserSerialized(id=participant.user.id, 
                                                     email=participant.user.email,
                                                     first_name=participant.user.first_name,
                                                     last_name=participant.user.last_name),
                                 score=participant.score)


# Read participants (search)
@router.get("/contests/{contest_id}/participants")
def read_participants(contest_id: int,
                      keywords: Optional[str] = None,
                      offset: int = Query(0, ge=0),
                      limit: int = Query(10, gt=0, le=100),
                      token: Optional[str] = Depends(oauth2_scheme),
                      session: Session = Depends(get_session)) -> List[ParticipantSerialized]:
    get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")

    query = select(Participant).join(User, Participant.user_id == User.id).where(Participant.contest_id == contest_id)
    if keywords:
        query = query.where((Participant.user.email.ilike(f"%{keywords}%")) |
                            (Participant.user.first_name.ilike(f"%{keywords}%")) |
                            (Participant.user.last_name.ilike(f"%{keywords}%")))
    
    participants = session.exec(query.offset(offset).limit(limit)).all()
    
    return [ParticipantSerialized(id=participant[0].id,
                                  user=UserSerialized(id=participant[0].user_id,
                                                      email=participant[0].user.email,
                                                      first_name=participant[0].user.first_name,
                                                      last_name=participant[0].user.last_name),
                                  score=participant[0].score) for participant in participants]


# Read my participant
@router.get("/contests/{contest_id}/participants/me")
def read_my_participant(contest_id: int,
                        token: Optional[str] = Depends(oauth2_scheme),
                        session: Session = Depends(get_session)) -> ParticipantSerialized:
    user = get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()
    if participant is None:
        raise HTTPException(status_code=404, detail="You are not signed up for this contest.")
    
    return ParticipantSerialized(id=participant.id,
                                 user=UserSerialized(id=participant.user_id,
                                                     email=participant.user.email,
                                                     first_name=participant.user.first_name,
                                                     last_name=participant.user.last_name),
                                 score=participant.score)


# Delete my participant (sign out of contest)
@router.delete("/contests/{contest_id}/participants/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_participant(contest_id: int,
                          token: Optional[str] = Depends(oauth2_scheme),
                          session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    if contest.start_date <= datetime.now().astimezone():
        raise HTTPException(status_code=403, detail="Can't sign out of contest after it has started.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()
    if participant is None:
        raise HTTPException(status_code=404, detail="You are not signed up for this contest.")
    
    session.delete(participant)
    session.commit()


# Read a participant
@router.get("/contests/{contest_id}/participants/{participant_id}")
def read_participant(contest_id: int,
                     participant_id: int,
                     token: Optional[str] = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> ParticipantSerialized:
    user = get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.id == participant_id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found.")
    
    return ParticipantSerialized(id=participant.id,
                                 user=UserSerialized(id=participant.user_id,
                                                     email=participant.user.email,
                                                     first_name=participant.user.first_name,
                                                     last_name=participant.user.last_name),
                                 score=participant.score)


# Score a participant
@router.post("/contests/{contest_id}/participants/{participant_id}/score")
def score_participant(contest_id: int,
                      participant_id: int,
                      request: ScoreParticipantForm,
                      token: Optional[str] = Depends(oauth2_scheme),
                      session: Session = Depends(get_session)) -> ParticipantSerialized:
    user = get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest_id))).scalar_one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="You are not an organizer of this contest.")
    
    participant = session.exec(select(Participant).where((Participant.id == participant_id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found.")
    
    participant.score = request.score
    session.add(participant)
    
    if participant.team_member is not None:
        team_participants = session.exec(select(TeamMember).where(TeamMember.team_id == participant.team_member.team_id)).all()
        for team_participant in team_participants:
            team_participant.score = request.score
            session.add(team_participant)
    
    session.commit()
    session.refresh(participant)
    
    return ParticipantSerialized(id=participant.id,
                                 user=UserSerialized(id=participant.user_id,
                                                     email=participant.user.email,
                                                     first_name=participant.user.first_name,
                                                     last_name=participant.user.last_name),
                                 score=participant.score)


# Delete a participant (kick)
@router.delete("/contests/{contest_id}/participants/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(contest_id: int,
                       participant_id: int,
                       token: Optional[str] = Depends(oauth2_scheme),
                       session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)

    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    organizer = session.exec(select(Organizer).where((Organizer.user_id == user.id) &
                                                     (Organizer.contest_id == contest_id))).scalar_one_or_none()
    if organizer is None:
        raise HTTPException(status_code=403, detail="You are not an organizer of this contest.")
    
    participant = session.exec(select(Participant).where((Participant.id == participant_id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()
    if participant is None:
        raise HTTPException(status_code=404, detail="Participant not found.")
    
    session.delete(participant)
    session.commit()


