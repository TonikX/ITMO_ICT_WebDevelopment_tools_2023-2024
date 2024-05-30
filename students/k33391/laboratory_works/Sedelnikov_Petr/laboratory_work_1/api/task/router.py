from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/task",
    tags=["Задания"]
)
auth = AuthHandler()


@router.get('')
def get_tasks(session=Depends(get_session), user=Depends(auth.get_current_user)):
    return session.query(Task).all()


@router.post('')
def create_task(
        task: CreateTask,
        session=Depends(get_session),
        user=Depends(auth.get_current_user)
):
    contest = session.get(Contest, task.contest_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    if user.id != contest.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    new_task = Task(
        contest_id=task.contest_id,
        name=task.name,
        description=task.description,
        requirements=task.requirements,
        criteria=task.criteria,
        user_id=user.id
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return {"status": 200, "data": new_task}


@router.get('/{task_id}')
def get_task(task_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    return task


@router.patch('')
def edit_task(new_task: EditTask, session=Depends(get_session), user=Depends(auth.get_current_user)):
    task = session.get(Task, new_task.id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    task_data = new_task.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(task, key, value)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete('/{task_id}')
def delete_task(task_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Not found")
    if task.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(task)
    session.commit()
    return {"ok": True}
