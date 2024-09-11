from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from schemas import Team, TeamDefault, TeamDisplay
from database import get_session
from typing_extensions import TypedDict

router = APIRouter(tags=["Team"])

@router.post("/team-create", status_code=status.HTTP_201_CREATED)
def team_create(team: TeamDefault, session=Depends(get_session)) -> Team:
    team = Team.model_validate(team)
    session.add(team)
    session.commit()
    session.refresh(team)
    return team


@router.get("/list-teams", status_code=status.HTTP_200_OK)
def teams_list(session=Depends(get_session)) -> list[Team]:
    return session.query(Team).all()


@router.get("/team/{team_id}", status_code=status.HTTP_200_OK, response_model=TeamDisplay)
def team_get(team_id: int, session=Depends(get_session)) -> Team:
    obj = session.get(Team, team_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="team not found")
    return obj


@router.patch("/team/update/{team_id}", status_code=status.HTTP_202_ACCEPTED)
def team_update(team_id: int, team: TeamDefault, session=Depends(get_session)) \
        -> Team:
    db_team = session.get(Team, team_id)
    if not db_team:
        raise HTTPException(status_code=404, detail="team not found")

    team_data = team.model_dump(exclude_unset=True)
    for key, value in team_data.items():
        setattr(db_team, key, value)
    session.add(db_team)
    session.commit()
    session.refresh(db_team)
    return db_team


@router.delete("/team/delete/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
def team_delete(team_id: int, session=Depends(get_session)):
    team = session.get(Team, team_id)
    if not team:
        raise HTTPException(status_code=404, detail="team not found")
    session.delete(team)
    session.commit()
    return {"ok": True}

