from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from schemas import TeamMemberDefault, TeamMember
from database import get_session
from typing_extensions import TypedDict

router = APIRouter(tags=["Team member"])

@router.post("/team_member-create", status_code=status.HTTP_201_CREATED)
def team_member_create(team_member: TeamMemberDefault, session=Depends(get_session)) -> TeamMember:
    team_member = TeamMember.model_validate(team_member)
    session.add(team_member)
    session.commit()
    session.refresh(team_member)
    return team_member


@router.get("/list-team_members", status_code=status.HTTP_200_OK)
def team_members_list(session=Depends(get_session)) -> list[TeamMember]:
    return session.query(TeamMember).all()


@router.get("/team_member/{team_member_id}", status_code=status.HTTP_200_OK)
def team_member_get(team_member_id: int, session=Depends(get_session)) -> TeamMember:
    obj = session.get(TeamMember, team_member_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="team_member not found")
    return obj


@router.patch("/team_member/update/{team_member_id}", status_code=status.HTTP_202_ACCEPTED)
def team_member_update(team_member_id: int, team_member: TeamMemberDefault, session=Depends(get_session)) \
        -> TeamMember:
    db_team_member = session.get(TeamMember, team_member_id)
    if not db_team_member:
        raise HTTPException(status_code=404, detail="team_member not found")

    team_member_data = team_member.model_dump(exclude_unset=True)
    for key, value in team_member_data.items():
        setattr(db_team_member, key, value)
    session.add(db_team_member)
    session.commit()
    session.refresh(db_team_member)
    return db_team_member


@router.delete("/team_member/delete/{team_member_id}", status_code=status.HTTP_204_NO_CONTENT)
def team_member_delete(team_member_id: int, session=Depends(get_session)):
    team_member = session.get(TeamMember, team_member_id)
    if not team_member:
        raise HTTPException(status_code=404, detail="team_member not found")
    session.delete(team_member)
    session.commit()
    return {"ok": True}

