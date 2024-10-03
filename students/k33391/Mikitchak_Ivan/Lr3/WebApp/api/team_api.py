from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from typing import List, Optional

from dependencies import oauth2_scheme
from connection import get_session
from utilities import get_user_by_token, generate_code
from models import (
    JoinTeamForm,
    TeamForm,
    Contest,
    Participant,
    Team,
    TeamMemberSerialized,
    TeamSerialized,
    TeamSerializedOwner,
    TeamMember,
    TeamRole,
    UserSerialized,
    )

from datetime import datetime


router = APIRouter()


# Create a team
@router.post("/contests/{contest_id}/teams", status_code=status.HTTP_201_CREATED)
def create_team(contest_id: int,
                request: TeamForm,
                token: Optional[str] = Depends(oauth2_scheme),
                session: Session = Depends(get_session)) -> TeamSerializedOwner:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    if contest.start_date <= datetime.now().astimezone():
        raise HTTPException(status_code=403, detail="Can't create a team after the start of the contest.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest.id))).one_or_none()
    if participant is None:
        raise HTTPException(status_code=400, detail="User is not signed up for this contest.")
    
    member = session.exec(select(TeamMember).where(TeamMember.participant_id == participant.id)).one_or_none()
    if member is not None:
        raise HTTPException(status_code=409, detail=f"User is already a member of a team {member.team_id}")    
       
    code = generate_code()
    team = Team(contest_id=contest.id, name=request.name, code=code)
    
    session.add(team)
    session.commit()
    session.refresh(team)
    
    member = TeamMember(participant=participant, team=team, role=TeamRole.owner)
    session.add(member)
    session.commit()
    
    return TeamSerializedOwner(id=team.id, name=team.name, code=team.code)


# Read teams (search)
@router.get("/contests/{contest_id}/teams")
def read_teams(contest_id: int,
               keywords: Optional[str] = None,
               offset: int = Query(0, ge=0),
               limit: int = Query(10, gt=0, le=100),
               token: Optional[str] = Depends(oauth2_scheme),
               session: Session = Depends(get_session)) -> List[TeamSerialized]:
    get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    query = select(Team).where(Team.contest_id == contest_id)
    if keywords is not None:
        query = query.where(Team.name.ilike(f"%{keywords}%"))
    
    teams = session.exec(query.offset(offset).limit(limit)).all()
    
    return [TeamSerialized(id=team.id, name=team.name) for team in teams]


# Read my team
@router.get("/contests/{contest_id}/teams/my")
def read_my_team(contest_id: int,
                 token: Optional[str] = Depends(oauth2_scheme),
                 session: Session = Depends(get_session)) -> TeamSerialized | TeamSerializedOwner:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")
    
    member = participant.team_member
    team = member.team
    
    if member.role == TeamRole.owner:
        return TeamSerializedOwner(id=team.id, name=team.name, code=team.code)
    else:
        return TeamSerialized(id=team.id, name=team.name)
    

# Update my team code
@router.post("/contests/{contest_id}/teams/my/update_code")
def update_my_team_code(contest_id: int,
                        token: Optional[str] = Depends(oauth2_scheme),
                        session: Session = Depends(get_session)) -> TeamSerializedOwner:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()        
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    member = participant.team_member
    team = member.team
    
    if member.role != TeamRole.owner:
        raise HTTPException(status_code=400, detail="Only team owner can update the team code.")
    
    team.code = generate_code()
    
    session.add(team)
    session.commit()
    session.refresh(team)
    
    return TeamSerializedOwner(id=team.id, name=team.name, code=team.code)


# Update my team (all fields except code)
@router.put("/contests/{contest_id}/teams/my")
def update_my_team(contest_id: int,
                   request: TeamForm,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)) -> TeamSerializedOwner:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()        
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    member = participant.team_member
    team = member.team
    
    if member.role != TeamRole.owner:
        raise HTTPException(status_code=400, detail="Only team owner can update a team.")
    
    if request.name:
        team.name = request.name
    
    session.add(team)
    session.commit()
    session.refresh(team)
    
    return TeamSerializedOwner(id=team.id, name=team.name, code=team.code)


# Delete my team
@router.delete("/contests/{contest_id}/teams/my", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_team(contest_id: int,
                   token: Optional[str] = Depends(oauth2_scheme),
                   session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()        
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    member = participant.team_member
    team = member.team
    
    if member.role != TeamRole.owner:
        raise HTTPException(status_code=400, detail="Only team owner can delete a team.")
    
    session.delete(team)
    session.commit()


# Read my team members (search)
@router.get("/contests/{contest_id}/teams/my/members")
def read_my_team_members(contest_id: int,
                         token: Optional[str] = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)) -> List[TeamMemberSerialized]:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()        
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    team = participant.team_member.team
    members = session.exec(select(TeamMember).where(TeamMember.team_id == team.id)).all()
    
    return [TeamMemberSerialized(id=member.id,
                                 user=UserSerialized(id=member.participant.user_id,
                                                     email=member.participant.user.email,
                                                     first_name=member.participant.user.first_name,
                                                     last_name=member.participant.user.last_name),
                                 role=member.role) for member in members]


# Read me as my team member
@router.get("/contests/{contest_id}/teams/my/members/me")
def read_my_team_members(contest_id: int,
                         token: Optional[str] = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)) -> TeamMemberSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()        
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    member = participant.team_member
    
    return TeamMemberSerialized(id=member.id,
                                user=UserSerialized(id=member.participant.user_id,
                                                    email=member.participant.user.email,
                                                    first_name=member.participant.user.first_name,
                                                    last_name=member.participant.user.last_name),
                                role=member.role)


# Delete me as my team member (leave team)
@router.delete("/contests/{contest_id}/teams/my/members/me", status_code=status.HTTP_204_NO_CONTENT)
def read_my_team_members(contest_id: int,
                         token: Optional[str] = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()        
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    member = participant.team_member
    
    session.delete(member)
    session.commit()


# Read my team member
@router.get("/contests/{contest_id}/teams/my/members/{member_id}")
def read_my_team_member(contest_id: int,
                         member_id: int,
                         token: Optional[str] = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)) -> TeamMemberSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")

    team = participant.team_member.team
    member = session.exec(select(TeamMember).where((TeamMember.team_id == team.id) &
                                                   (TeamMember.id == member_id))).one_or_none()
    if member is None:
        raise HTTPException(status_code=404, detail="Team member not found.")
    
    return TeamMemberSerialized(id=member.id,
                                user=UserSerialized(id=member.participant.user_id,
                                                    email=member.participant.user.email,
                                                    first_name=member.participant.user.first_name,
                                                    last_name=member.participant.user.last_name),
                                role=member.role)


# Delete my team member (kick)
@router.delete("/contests/{contest_id}/teams/my/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_my_team_member(contest_id: int,
                         member_id: int,
                         token: Optional[str] = Depends(oauth2_scheme),
                         session: Session = Depends(get_session)):
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    if participant.team_member is None:
        raise HTTPException(status_code=404, detail="User is not a member of any team.")
    if participant.team_member.role != TeamRole.owner:
        raise HTTPException(status_code=403, detail="Only owners can kick team members.")

    team = participant.team_member.team    
    member = session.exec(select(TeamMember).where((TeamMember.team_id == team.id) &
                                                   (TeamMember.id == member_id))).one_or_none()
    if member is None:
        raise HTTPException(status_code=404, detail="Team member not found.")
    
    session.delete(member)
    session.commit()


# Read a team
@router.get("/contests/{contest_id}/teams/{team_id}")
def retrieve_team(contest_id: int,
                  team_id: int,
                  token: Optional[str] = Depends(oauth2_scheme),
                  session: Session = Depends(get_session)) -> TeamSerialized:
    get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    team = session.exec(select(Team).where((Team.id == team_id) &
                                           (Team.contest_id == contest_id))).one_or_none()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found.")
    
    return TeamSerialized(id=team_id, name=team.name)


# Create a team member (join team)
@router.post("/contests/{contest_id}/teams/{team_id}/members", status_code=status.HTTP_201_CREATED)
def create_team_member(contest_id: int,
                       team_id: int,
                       request: JoinTeamForm,
                       token: Optional[str] = Depends(oauth2_scheme),
                       session: Session = Depends(get_session)) -> TeamMemberSerialized:
    user = get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    participant = session.exec(select(Participant).where((Participant.user_id == user.id) &
                                                         (Participant.contest_id == contest_id))).one_or_none()
    if participant is None:
        raise HTTPException(status_code=403, detail="User is not signed up for this contest.")
    
    team = session.exec(select(Team).where((Team.id == team_id) &
                                           (Team.contest_id == contest_id))).one_or_none()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found.")
    
    if request.code != team.code:
        raise HTTPException(status_code=403, detail="Incorrect team code.")
    
    member = TeamMember(participant=participant, team=team, role=TeamRole.member)
    
    session.add(member)
    session.commit()
    session.refresh(member)
    
    return TeamMemberSerialized(id=member.id,
                                user=UserSerialized(id=member.participant.user_id,
                                                    email=member.participant.user.email,
                                                    first_name=member.participant.user.first_name,
                                                    last_name=member.participant.user.last_name),
                                role=member.role)


# Read team members
@router.get("/contests/{contest_id}/teams/{team_id}/members")
def read_team_member(contest_id: int,
                     team_id: int,
                     token: Optional[str] = Depends(oauth2_scheme),
                     session: Session = Depends(get_session)) -> List[TeamMemberSerialized]:
    get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    team = session.exec(select(Team).where((Team.id == team_id) &
                                           (Team.contest_id == contest_id))).one_or_none()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found.")
    
    members = session.exec(select(TeamMember).where(TeamMember.team_id == team.id))
    
    return [TeamMemberSerialized(id=member.id,
                                 user=UserSerialized(id=member.participant.user_id,
                                                     email=member.participant.user.email,
                                                     first_name=member.participant.user.first_name,
                                                     last_name=member.participant.user.last_name),
                                 role=member.role) for member in members]


# Read a team member
@router.get("/contests/{contest_id}/teams/{team_id}/members/{member_id}")
def read_team_member(contest_id: int,
                       team_id: int,
                       member_id: int,
                       token: Optional[str] = Depends(oauth2_scheme),
                       session: Session = Depends(get_session)) -> TeamMemberSerialized:
    get_user_by_token(token, session)
    
    contest = session.exec(select(Contest).where(Contest.id == contest_id)).one_or_none()
    if contest is None:
        raise HTTPException(status_code=404, detail="Contest not found.")
    
    team = session.exec(select(Team).where((Team.id == team_id) &
                                           (Team.contest_id == contest_id))).one_or_none()
    if team is None:
        raise HTTPException(status_code=404, detail="Team not found.")
    
    member = session.exec(select(TeamMember).where((TeamMember.team_id == team.id) &
                                                   (TeamMember.id == member_id))).one_or_none()
    if member is None:
        raise HTTPException(status_code=404, detail="Team member not found.")
    
    return TeamMemberSerialized(id=member.id,
                                user=UserSerialized(id=member.participant.user_id,
                                                    email=member.participant.user.email,
                                                    first_name=member.participant.user.first_name,
                                                    last_name=member.participant.user.last_name),
                                role=member.role)
