from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select
from typing_extensions import TypedDict
from models import Tag, TagDefault
from connection import get_session

router = APIRouter()

@router.get("/")
def tags_list(session=Depends(get_session)) -> List[Tag]:
    return session.exec(select(Tag)).all()

@router.get("/{tag_id}")
def get_tag(tag_id: int, session=Depends(get_session)) -> Tag:
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag

@router.post("/")
def tag_create(tag: TagDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Tag}):
    tag = Tag.model_validate(tag)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return {"status": 200, "data": tag}

@router.delete("/{tag_id}")
def delete_tag(tag_id: int, session=Depends(get_session)) -> TypedDict('Response', {"is_deleted": bool}):
    tag = session.get(Tag, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    session.delete(tag)
    session.commit()
    return {"is_deleted": True}

@router.patch("/{tag_id}")
def update_tag(tag_id: int, tag: TagDefault, session=Depends(get_session)) -> Tag:
    db_tag = session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_data = tag.model_dump(exclude_unset=True)
    for key, value in tag_data.items():
        setattr(db_tag, key, value)
    session.add(db_tag)
    session.commit()
    session.refresh(db_tag)
    return db_tag
