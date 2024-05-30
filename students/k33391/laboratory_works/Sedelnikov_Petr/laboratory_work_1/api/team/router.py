from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/team",
    tags=["Команды"]
)
auth = AuthHandler()


@router.get('')
def get_teams(session=Depends(get_session), user=Depends(auth.get_current_user)):
    return session.query(Team).all()


@router.post('')
def create_team(
        team: CreateTeam,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    new_team = Team(
        name=team.name,
        user_id=user.id
    )
    session.add(new_team)
    session.commit()
    session.refresh(new_team)
    return {"status": 200, "data": new_team}


@router.get('/{team_id}')
def get_team(team_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    return team


@router.patch('')
def edit_team(new_team: EditTeam, session=Depends(get_session), user=Depends(auth.get_current_user)):
    team = session.get(Team, new_team.id)
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    if team.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    team_data = new_team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(team, key, value)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.delete('/{team_id}')
def delete_team(team_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Not found")
    if team.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(team)
    session.commit()
    return {"ok": True}
