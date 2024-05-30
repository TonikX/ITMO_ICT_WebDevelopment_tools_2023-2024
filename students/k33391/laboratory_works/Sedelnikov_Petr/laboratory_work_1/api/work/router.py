from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/work",
    tags=["Работы"]
)
auth = AuthHandler()


@router.get('')
def get_works(session=Depends(get_session), user=Depends(auth.get_current_user)):
    return session.query(Work).all()


@router.post('')
def create_work(
        work: CreateWork,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    task = session.get(Task, work.task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    new_work = Work(
        task_id=work.task_id,
        description=work.description,
        user_id=user.id
    )
    session.add(new_work)
    session.commit()
    session.refresh(new_work)
    return {"status": 200, "data": new_work}


@router.get('/{work_id}')
def get_work(work_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    work = session.get(Work, work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Not found")
    return work


@router.patch('')
def edit_work(new_work: EditWork, session=Depends(get_session), user=Depends(auth.get_current_user)):
    work = session.get(Work, new_work.id)
    if not work:
        raise HTTPException(status_code=404, detail="Not found")
    if work.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    work_data = new_work.model_dump(exclude_unset=True)
    for key, value in work_data.items():
        setattr(work, key, value)
    session.add(work)
    session.commit()
    session.refresh(work)
    return work


@router.delete('/{work_id}')
def delete_work(work_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    work = session.get(Work, work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Not found")
    if work.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(work)
    session.commit()
    return {"ok": True}
