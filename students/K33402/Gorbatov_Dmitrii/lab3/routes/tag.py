from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from connection import get_session
from models import Tag

router = APIRouter()

@router.get("/tag", response_model=List[Tag], tags=["tag"])
def tag_list(session=Depends(get_session)) -> List[Tag]:
    return session.exec(select(Tag)).all()

@router.get("/tag/{tag_id}", response_model=Tag, tags=["tag"])
def tag_read(tag_id: int, session=Depends(get_session)) -> Tag:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.patch("/tag/{tag_id}", response_model=Tag, tags=["tag"])
def tag_update(tag_id: int, tag: Tag, session=Depends(get_session)) -> Tag:
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_data = tag.dict(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(db_tag, key, value)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag

@router.delete("/tag/{tag_id}", tags=["tag"])
def tag_delete(tag_id: int, session=Depends(get_session)):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return {"ok": True}

@router.post("/tag", response_model=Tag, tags=["tag"])
def create_tag(tag: Tag, session=Depends(get_session)) -> Tag:
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag
