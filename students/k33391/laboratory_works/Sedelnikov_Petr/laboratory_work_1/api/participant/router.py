from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/participant",
    tags=["Участники"]
)
auth = AuthHandler()


@router.get('')
def get_participants(session=Depends(get_session), user=Depends(auth.get_current_user)):
    participants = []
    for participant in session.query(Participant).all():
        new_participant = GetParticipant(
            id=participant.id,
            user_id=participant.user_id,
            contest_id=participant.contest_id,
            name=participant.name,
            email=participant.email,
            phone=participant.phone
        )

        approval = session.query(ParticipantApprovals).filter(
            ParticipantApprovals.participant_id == participant.id,
        ).first()
        if approval:
            new_participant.is_approval = True
        participants.append(new_participant)
    return participants


@router.post('')
def create_participant(
        participant: CreateParticipant,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    participant_presence = session.query(Participant).filter(
        Participant.user_id == user.id,
        Participant.contest_id == participant.contest_id,
    ).all()
    if len(participant_presence) != 0:
        raise HTTPException(status_code=400, detail="Already exists")
    contest = session.get(Contest, participant.contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    new_participant = Participant(
        contest_id=participant.contest_id,
        name=participant.name,
        email=participant.email,
        phone=participant.phone,
        user_id=user.id
    )
    session.add(new_participant)
    session.commit()
    session.refresh(new_participant)
    return {"status": 200, "data": new_participant}


@router.get('/{participant_id}')
def get_participant(participant_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Not found")
    new_participant = GetParticipant(
        id=participant.id,
        user_id=participant.user_id,
        contest_id=participant.contest_id,
        name=participant.name,
        email=participant.email,
        phone=participant.phone
    )

    approval = session.query(ParticipantApprovals).filter(
        ParticipantApprovals.participant_id == participant.id,
    ).first()
    if approval:
        new_participant.is_approval = True
    return new_participant


@router.patch('')
def edit_participant(new_participant: EditParticipant, session=Depends(get_session), user=Depends(auth.get_current_user)):
    participant = session.get(Participant, new_participant.id)
    if not participant:
        raise HTTPException(status_code=404, detail="Not found")
    if participant.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    contest = session.get(Contest, participant.contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    participant_data = new_participant.model_dump(exclude_unset=True)
    for key, value in participant_data.items():
        setattr(participant, key, value)
    session.add(participant)
    session.commit()
    session.refresh(participant)
    return participant


@router.delete('/{participant_id}')
def delete_participant(participant_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    participant = session.get(Participant, participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Not found")
    if participant.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(participant)
    session.commit()
    return {"ok": True}