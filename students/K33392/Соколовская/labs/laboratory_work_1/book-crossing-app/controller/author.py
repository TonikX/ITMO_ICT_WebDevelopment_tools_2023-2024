from typing import List

from fastapi import HTTPException, Depends, APIRouter
from sqlmodel import select, Session

from connection import get_session
from models import Author, AuthorOut, AuthorIn

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("", response_model=List[AuthorOut])
def authors_list(session: Session = Depends(get_session)):
    authors = session.exec(select(Author)).all()
    return authors


@router.get("/{author_id}", response_model=AuthorOut)
def author_get(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.post("", response_model=AuthorOut)
def author_create(author: AuthorIn, session: Session = Depends(get_session)):
    author = Author.model_validate(author)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.patch("/{author_id}", response_model=AuthorOut)
def author_update(author_id: int, updated_author: AuthorIn, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    for key, value in updated_author.model_dump(exclude_unset=True).items():
        setattr(author, key, value)
    session.add(author)
    session.commit()
    session.refresh(author)
    return author


@router.delete("/{author_id}", response_model=dict)
def author_delete(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"message": "Author deleted successfully"}
