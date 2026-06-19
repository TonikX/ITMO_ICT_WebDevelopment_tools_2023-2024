"""API хакатонов."""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, require_role
from app.models import Hackathon, User, UserRole
from app.schemas import HackathonCreate, HackathonOut

router = APIRouter(prefix="/hackathons", tags=["Хакатоны"])


@router.post("", response_model=HackathonOut, status_code=status.HTTP_201_CREATED)
def create_hackathon(
    data: HackathonCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organizer)),
):
    """Создание хакатона (только организатор)."""
    hackathon = Hackathon(**data.model_dump())
    db.add(hackathon)
    db.commit()
    db.refresh(hackathon)
    return hackathon


@router.get("", response_model=List[HackathonOut])
def list_hackathons(db: Session = Depends(get_db)):
    """Список всех хакатонов (доступен без авторизации)."""
    return db.query(Hackathon).all()


@router.get("/{hackathon_id}", response_model=HackathonOut)
def get_hackathon(hackathon_id: int, db: Session = Depends(get_db)):
    hackathon = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Хакатон не найден"
        )
    return hackathon


@router.delete("/{hackathon_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hackathon(
    hackathon_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.organizer)),
):
    hackathon = db.query(Hackathon).filter(Hackathon.id == hackathon_id).first()
    if hackathon is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Хакатон не найден"
        )
    db.delete(hackathon)
    db.commit()
