from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/member",
    tags=["Участники команд"]
)
auth = AuthHandler()


@router.post('')
def create_member(
        member: CreateTeamMember,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    member_presence = session.query(TeamMember).filter(
        TeamMember.team_id == member.team_id,
        TeamMember.user_id == user.id,
    ).all()
    if len(member_presence) != 0:
        raise HTTPException(status_code=400, detail="Already exists")
    team = session.get(Team, member.team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    new_member = TeamMember(
        team_id=member.team_id,
        user_id=user.id
    )
    session.add(new_member)
    session.commit()
    session.refresh(new_member)
    return {"status": 200, "data": new_member}


@router.delete('')
def delete_member(
        member: DeleteTeamMember,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    member = session.query(TeamMember).filter(
        TeamMember.team_id == member.team_id,
        TeamMember.user_id == user.id,
    ).first()
    if not member:
        raise HTTPException(status_code=404, detail="Not found")
    session.delete(member)
    session.commit()
    return {"ok": True}

