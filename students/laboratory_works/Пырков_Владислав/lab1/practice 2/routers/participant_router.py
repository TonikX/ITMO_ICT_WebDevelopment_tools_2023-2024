from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from schemas import Participant, ParticipantDefault, ParticipantDisplay
from database import get_session
from typing_extensions import TypedDict

router = APIRouter(tags=["Participant"])

@router.post("/participant-create", status_code=status.HTTP_201_CREATED)
def participant_create(participant: ParticipantDefault, session=Depends(get_session)) -> Participant:
    participant = Participant.model_validate(participant)
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return participant


@router.get("/list-participants", status_code=status.HTTP_200_OK)
def participants_list(session=Depends(get_session)) -> list[Participant]:
    return session.query(Participant).all()


@router.get("/participant/{participant_id}", status_code=status.HTTP_200_OK, response_model=ParticipantDisplay)
def participant_get(participant_id: int, session=Depends(get_session)):
    obj = session.get(Participant, participant_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="participant not found")
    return obj


@router.patch("/participant/update/{participant_id}", status_code=status.HTTP_202_ACCEPTED)
def participant_update(participant_id: int, participant: ParticipantDefault, session=Depends(get_session)) \
        -> Participant:
    db_participant = session.get(Participant, participant_id)
    if not db_participant:
        raise HTTPException(status_code=404, detail="participant not found")

    participant_data = participant.model_dump(exclude_unset=True)
    for key, value in participant_data.items():
        setattr(db_participant, key, value)
    session.add(db_participant)
    session.commit()
    session.refresh(db_participant)
    return db_participant


@router.delete("/participant/delete/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def participant_delete(participant_id: int, session=Depends(get_session)):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="participant not found")
    session.delete(participant)
    session.commit()
    return {"ok": True}

