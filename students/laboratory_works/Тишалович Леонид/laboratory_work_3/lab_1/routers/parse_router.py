from fastapi import APIRouter, HTTPException
from fastapi import Depends, status
from schemas import Site
from database import get_session

router = APIRouter(tags=["Parse"])

@router.get("/get-tasks/")
def cases_list(session=Depends(get_session)) -> list[Site]:
    return session.query(Site).all()