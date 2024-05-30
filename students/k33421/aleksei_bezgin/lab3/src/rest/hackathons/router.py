from fastapi import APIRouter, HTTPException
from sqlmodel import select

from db.models import Hackathon as HackathonModel
from rest.dependencies import DatabaseSession
from rest.hackathons.schemas import Hackathon, HackathonCreateData, HackathonUpdateData

router = APIRouter()


@router.get("/")
def get_hackathons(session: DatabaseSession) -> list[Hackathon]:
    stmt = select(HackathonModel)
    return session.scalars(stmt).all()


@router.get("/{hackathon_id}")
def get_hackathon(hackathon_id: int, session: DatabaseSession) -> Hackathon:
    stmt = select(HackathonModel).where(HackathonModel.id == hackathon_id)
    return session.scalars(stmt).first()


@router.post("/")
def create_hackathon(hackathon_data: HackathonCreateData, session: DatabaseSession) -> Hackathon:
    hackathon_model = HackathonModel.model_validate(hackathon_data)
    session.add(hackathon_model)
    session.commit()
    session.refresh(hackathon_model)

    return hackathon_model


@router.patch("/{hackathon_id}")
def update_hackathon(hackathon_id: int, hackathon_data: HackathonUpdateData, session: DatabaseSession) -> Hackathon:
    stmt = select(HackathonModel).where(HackathonModel.id == hackathon_id)
    hackathon_model = session.scalars(stmt).first()

    for key, value in hackathon_data.model_dump(exclude_unset=True).items():
        setattr(hackathon_model, key, value)

    session.add(hackathon_model)
    session.commit()
    session.refresh(hackathon_model)

    return hackathon_model


@router.delete("/{hackathon_id}")
def delete_hackathon(hackathon_id: int, session: DatabaseSession) -> str:
    stmt = select(HackathonModel).where(HackathonModel.id == hackathon_id)
    hackathon_model = session.scalars(stmt).first()
    if not hackathon_model:
        raise HTTPException(status_code=404, detail="Hackathon not found")

    session.delete(hackathon_model)
    session.commit()

    return f"Hackathon {hackathon_model.name} deleted"