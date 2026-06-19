"""API команд: создание, вступление, состав (демонстрация связи many-to-many)."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import Hackathon, Team, TeamMember, User
from app.schemas import TeamCreate, TeamDetailOut, TeamJoin, TeamMemberOut, TeamOut

router = APIRouter(prefix="/teams", tags=["Команды"])


@router.post("", response_model=TeamDetailOut, status_code=status.HTTP_201_CREATED)
def create_team(
    data: TeamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Создать команду. Создатель автоматически становится участником."""
    hackathon = db.query(Hackathon).filter(Hackathon.id == data.hackathon_id).first()
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Хакатон не найден"
        )

    team = Team(name=data.name, description=data.description, hackathon_id=data.hackathon_id)
    db.add(team)
    try:
        db.flush()  # получаем team.id, проверяем уникальность имени
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Команда с таким именем уже есть на этом хакатоне",
        )

    membership = TeamMember(
        user_id=current_user.id, team_id=team.id, role_in_team=data.role_in_team
    )
    db.add(membership)
    db.commit()
    db.refresh(team)
    return team


@router.get("", response_model=List[TeamOut])
def list_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()


@router.get("/{team_id}", response_model=TeamDetailOut)
def get_team(team_id: int, db: Session = Depends(get_db)):
    """Команда с полным составом участников (связь many-to-many)."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")
    return team


@router.post("/{team_id}/join", response_model=TeamMemberOut, status_code=status.HTTP_201_CREATED)
def join_team(
    team_id: int,
    data: TeamJoin,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Присоединиться к команде, указав свою роль (характеризующее поле связи)."""
    team = db.query(Team).filter(Team.id == team_id).first()
    if team is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Команда не найдена")

    already = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == current_user.id)
        .first()
    )
    if already:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Вы уже состоите в этой команде"
        )

    membership = TeamMember(
        user_id=current_user.id, team_id=team_id, role_in_team=data.role_in_team
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.delete("/{team_id}/leave", status_code=status.HTTP_204_NO_CONTENT)
def leave_team(
    team_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    membership = (
        db.query(TeamMember)
        .filter(TeamMember.team_id == team_id, TeamMember.user_id == current_user.id)
        .first()
    )
    if membership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вы не состоите в этой команде"
        )
    db.delete(membership)
    db.commit()
