from fastapi import APIRouter, HTTPException, Depends
from auth import AuthHandler
from models import *
from connection import get_session
from starlette.responses import JSONResponse
from starlette.status import HTTP_201_CREATED

router = APIRouter(
    prefix="/grade",
    tags=["Оценки"]
)
auth = AuthHandler()


@router.get('')
def get_grades(session=Depends(get_session), user=Depends(auth.get_current_user)):
    return session.query(WorkGrade).all()


@router.post('')
def create_grade(grade: CreateWorkGrade, session=Depends(get_session), user=Depends(auth.get_current_user)):
    work = session.get(Work, grade.work_id)
    if not work:
        raise HTTPException(status_code=404, detail="Not found")
    new_grade = WorkGrade(
        work_id=grade.work_id,
        grade=grade.grade,
        description=grade.description,
        user_id=user.id
    )
    session.add(new_grade)
    session.commit()
    session.refresh(new_grade)
    return {"status": 200, "data": new_grade}


@router.get('/{grade_id}')
def get_grade(grade_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    contest = session.get(WorkGrade, grade_id)
    if not contest:
        raise HTTPException(status_code=404, detail="Not found")
    return contest


@router.patch('')
def edit_grade(new_grade: EditWorkGrade, session=Depends(get_session), user=Depends(auth.get_current_user)):
    grade = session.get(WorkGrade, new_grade.id)
    if not grade:
        raise HTTPException(status_code=404, detail="Not found")
    if grade.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    grade_data = new_grade.model_dump(exclude_unset=True)
    for key, value in grade_data.items():
        setattr(grade, key, value)
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


@router.delete('/{grade_id}')
def delete_grade(grade_id: int, session=Depends(get_session), user=Depends(auth.get_current_user)):
    grade = session.get(WorkGrade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Not found")
    if grade.user_id != user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    session.delete(grade)
    session.commit()
    return {"ok": True}