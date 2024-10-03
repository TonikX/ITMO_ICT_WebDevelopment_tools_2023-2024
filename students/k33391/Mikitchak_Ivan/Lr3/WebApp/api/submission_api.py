from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlmodel import Session

from typing import List, Literal, Optional

from dependencies import oauth2_scheme
from connection import get_session
from utilities import get_user_by_token
from models import (
    Contest,
    Organizer,
    Participant,
    ParticipantSerialized,
    Problem,
    Submission,
    SubmissionForm,
    SubmissionSerialized,
    SubmissionSerializedMy,
    SubmissionSerializedMyShort,
    SubmissionSerializedShort,
    SubmissionSerializedTeam,
    SubmissionSerializedTeamShort,
    TeamMember,
    TeamMemberSerialized,
    User,
    UserSerialized,
    )

from datetime import datetime


router = APIRouter()


# Create a submission (upload a solution)
@router.post("/contests/{contest_id}/problems/{problem_id}/submissions", status_code=status.HTTP_201_CREATED)
def create_submission(contest_id: int,
                      problem_id: int,
                      request: SubmissionForm,
                      token: Optional[str] = Depends(oauth2_scheme),
                      session: Session = Depends(get_session)) -> SubmissionSerializedMy:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    if datetime.now().astimezone() < contest.start_date or datetime.now().astimezone() > contest.end_date:
        raise HTTPException(status_code=403, detail="Can create submissions only during the contest.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest.id))).scalar_one_or_none()
    if participant is None:
        raise HTTPException(status_code=400, detail="User is not signed up for this contest.")
    
    problem = session.exec(select(Problem).where((Problem.contest_id == contest_id) &
                                                 (Problem.id == problem_id))).scalar_one_or_none()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    
    submission = Submission(problem=problem, participant=participant, data=request.data)
    
    session.add(submission)
    session.commit()
    session.refresh(submission)
    
    return SubmissionSerializedMy(id=submission.id, data=submission.data, date_submitted=submission.date_submitted)


# Read submissions (search, show all, filter mine, filter team's)
@router.get("/contests/{contest_id}/problems/{problem_id}/submissions")
def read_submissions(contest_id: int,
                      problem_id: int,
                      mode: Literal["all", "my", "team"] = "all",
                      author: Optional[str] = None,
                      content: Optional[str] = None,
                      offset: int = Query(0, ge=0),
                      limit: int = Query(10, gt=0, le=100),
                      date_st: Optional[datetime] = None,
                      date_end: Optional[datetime] = None,
                      token: Optional[str] = Depends(oauth2_scheme),
                      session: Session = Depends(get_session)) -> List[SubmissionSerializedShort |
                                                                       SubmissionSerializedMyShort |
                                                                       SubmissionSerializedTeamShort]:
    if date_st is not None and date_end is not None and date_st >= date_end:
        raise HTTPException(status_code=400, detail="The date_st must be earlier than the date_end.")
    
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.user_id == user.id))).scalar_one_or_none() 
    if organizer is None and participant is None:
        raise HTTPException(status_code=403, detail="User is neither participant nor organizer of this contest.")
    
    if organizer is None and datetime.now().astimezone() < contest.start_date or datetime.now().astimezone() > contest.end_date:
        raise HTTPException(status_code=403, detail="Can't access submissions before the start of the contest.")
    
    problem = session.exec(select(Problem).where((Problem.contest_id == contest_id) &
                                                 (Problem.id == problem_id))).scalar_one_or_none() 
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    
    query = select(Submission).where(Submission.problem_id == problem_id)\
        .join(Participant, Submission.participant_id == Participant.id)\
        .join(User, Participant.user_id == User.id)

    if author is not None:
        query = query.where((User.first_name.ilike(f"%{author}%") |
                            User.last_name.ilike(f"%{author}%")))
    if content is not None:
        query = query.where(Submission.data.ilike(f"%{content}%"))
    if date_st is not None:
        query = query.where(Submission.date_submitted >= date_st)
    if date_end is not None:
        query = query.where(Submission.date_submitted <= date_end)
    
    if mode == "all":
        if organizer is None:
            raise HTTPException(status_code=403, detail="Only organizer can access all submissions.")
        
        submissions = session.exec(query.offset(offset).limit(limit)).all()
        
        return [SubmissionSerializedShort(id=submission[0].id,
                                          participant=ParticipantSerialized(id=submission[0].participant.id,
                                                                            user=UserSerialized(id=submission[0].participant.user_id,
                                                                                                email=submission[0].participant.user.email,
                                                                                                first_name=submission[0].participant.user.first_name,
                                                                                                last_name=submission[0].participant.user.last_name),
                                                                            score=submission[0].participant.score),
                                          date_submitted=submission[0].date_submitted) for submission in submissions]
    elif mode == "my":
        if participant is None:
            raise HTTPException(status_code=403, detail="User is not signed up for this contest.")        
        query = query.where(Submission.participant_id == participant.id)
        submissions = session.exec(query.offset(offset).limit(limit)).all()
        
        return [SubmissionSerializedMyShort(id=submission[0].id, date_submitted=submission[0].date_submitted) for submission in submissions]
    else:
        if participant is None:
            raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
        if participant.team_member is None:
            raise HTTPException(status_code=403, detail="User is not a member of any team.")
        team = participant.team_member.team
        query = query.join(TeamMember, TeamMember.participant_id == Participant.id)\
                 .where(TeamMember.team_id == team.id)
        submissions = session.exec(query.offset(offset).limit(limit)).all()
        
        return [SubmissionSerializedTeamShort(id=submission[0].id,
                                              member=TeamMemberSerialized(id=submission[0].participant.team_member.id,
                                                                          user=UserSerialized(id=submission[0].participant.user_id,
                                                                                              email=submission[0].participant.user.email,
                                                                                              first_name=submission[0].participant.user.first_name,
                                                                                              last_name=submission[0].participant.user.last_name),
                                                                          role=submission[0].participant.team_member.role),
                                              date_submitted=submission[0].date_submitted) for submission in submissions]


@router.get("/contests/{contest_id}/problems/{problem_id}/submissions/{submission_id}")
def read_submission(contest_id: int,
                    problem_id: int,
                    submission_id: int,
                    token: Optional[str] = Depends(oauth2_scheme),
                    session: Session = Depends(get_session)) -> SubmissionSerialized | SubmissionSerializedMy | SubmissionSerializedTeam:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).scalar_one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).scalar_one_or_none()    
    organizer = session.exec(select(Organizer).where((Organizer.contest_id == contest_id) &
                                                     (Organizer.user_id == user.id))).scalar_one_or_none()
    if organizer is None and participant is None:
        raise HTTPException(status_code=403, detail="User is neither participant nor organizer of this contest.")
    
    if organizer is None and datetime.now().astimezone() < contest.start_date or datetime.now().astimezone() > contest.end_date:
        raise HTTPException(status_code=403, detail="Can't access submissions before the start of the contest.")
    
    problem = session.exec(select(Problem).where((Problem.contest_id == contest_id) &
                                                 (Problem.id == problem_id))).scalar_one_or_none()
    if problem is None:
        raise HTTPException(status_code=404, detail="Problem not found.")
    
    submission = session.exec(select(Submission).where((Submission.problem_id == problem_id) &
                                                       (Submission.id == submission_id))).scalar_one_or_none()
    if organizer is not None:
        return SubmissionSerialized(id=submission.id,
                                    participant=ParticipantSerialized(id=submission.participant.id,
                                                                      user=UserSerialized(id=submission.participant.user_id,
                                                                                          email=submission.participant.user.email,
                                                                                          first_name=submission.participant.user.first_name,
                                                                                          last_name=submission.participant.user.last_name),
                                                                      score=submission.participant.score),
                                    data=submission.data,
                                    date_submitted=submission.date_submitted)
    elif submission.participant_id == participant.id:
        return SubmissionSerializedMy(id=submission.id, data=submission.data, date_submitted=submission.date_submitted)
    elif (submission.participant.team_member is not None and
          participant.team_member is not None and
          submission.participant.team_member.team_id == participant.team_member.team_id):
        return SubmissionSerializedTeam(id=submission.id,
                                        member=TeamMemberSerialized(id=submission.participant.team_member.id,
                                                                    user=UserSerialized(id=submission.participant.user_id,
                                                                                        email=submission.participant.user.email,
                                                                                        first_name=submission.participant.user.first_name,
                                                                                        last_name=submission.participant.user.last_name),
                                                                    role=submission.participant.team_member.role),
                                              data=submission.data,
                                              date_submitted=submission.date_submitted)
