from fastapi import APIRouter, HTTPException
from fastapi import Depends
from database import get_session
from models import Parse

parse_router = APIRouter()


@parse_router.get("/check/")
def cases_list(session=Depends(get_session)) -> list[Parse]:
    return session.query(Parse).all()