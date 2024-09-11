from fastapi import APIRouter, HTTPException
from fastapi import Depends
from db import get_session
from schemas import Parce

logic_router = APIRouter()


@logic_router.get("/check/")
def cases_list(session=Depends(get_session)) -> list[Parce]:
    return session.query(Parce).all()