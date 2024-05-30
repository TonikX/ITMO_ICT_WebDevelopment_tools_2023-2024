from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/approval",
    tags=["Утверждения"]
)
auth = AuthHandler()


@router.post('')
def create_approval(
        approval: CreateParticipantApproval,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    approval_presence = session.query(ParticipantApprovals).filter(
        ParticipantApprovals.participant_id == approval.participant_id,
    ).all()
    if len(approval_presence) != 0:
        raise HTTPException(status_code=400, detail="Already exists")
    participant = session.get(Participant, approval.participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Not found")
    contest = session.get(Contest, participant.contest_id)
    if contest.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    new_approval = ParticipantApprovals(
        participant_id=approval.participant_id,
        user_id=user.id
    )
    session.add(new_approval)
    session.commit()
    session.refresh(new_approval)
    return {"status": 200, "data": new_approval}


@router.delete('')
def delete_approval(
        approval: DeleteParticipantApproval,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    approval = session.query(ParticipantApprovals).filter(
        ParticipantApprovals.participant_id == approval.participant_id,
    ).first()
    if not approval:
        raise HTTPException(status_code=404, detail="Not found")
    participant = session.get(Participant, approval.participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Not found")
    contest = session.get(Contest, participant.contest_id)
    if contest.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(approval)
    session.commit()
    return {"ok": True}

