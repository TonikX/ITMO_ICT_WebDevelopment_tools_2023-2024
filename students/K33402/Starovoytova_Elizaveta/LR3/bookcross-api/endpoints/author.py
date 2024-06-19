from fastapi import APIRouter, HTTPException
from sqlmodel import select
from fastapi import Depends
from models import Author, AuthorBase, AuthorReadFull
from database.conn import get_session

author_router = APIRouter()


@author_router.get("/")
def get_authors(session=Depends(get_session)) -> list[Author]:
    return session.exec(select(Author)).all()


@author_router.get("/{author_id}")
def get_author(author_id: int, session=Depends(get_session)) -> AuthorReadFull:
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@author_router.post("/")
def create_author(author_data: AuthorBase, session=Depends(get_session)) -> Author:
    author = Author.model_validate(author_data)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

