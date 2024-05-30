from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/contest",
    tags=["Хакатоны"]
)
auth = AuthHandler()


@router.get('')
def get_contests(session=Depends(get_session), user=Depends(auth.get_current_user)):
    return session.query(Contest).all()


@router.post('')
def create_contest(contest: CreateContest, session=Depends(get_session), user=Depends(auth.get_current_user)):
    new_contest = Contest(
        name=contest.name,
        description=contest.description,
        start_time=contest.start_time,
        end_time=contest.end_time,
        user_id=user.id
    )
    session.add(new_contest)
    session.commit()
    session.refresh(new_contest)
    return {"status": 200, "data": new_contest}


@router.get('/{contest_id}')
def get_contest(contest_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    contest = session.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    return contest


@router.patch('')
def edit_contest(new_contest: EditContest, session=Depends(get_session), user=Depends(auth.get_current_user)):
    contest = session.get(Contest, new_contest.id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    if contest.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    contest_data = new_contest.model_dump(exclude_unset=True)
    for key, value in contest_data.items():
        setattr(contest, key, value)
    session.add(contest)
    session.commit()
    session.refresh(contest)
    return contest


@router.delete('/{contest_id}')
def delete_contest(contest_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    contest = session.get(Contest, contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    if contest.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(contest)
    session.commit()
    return {"ok": True}