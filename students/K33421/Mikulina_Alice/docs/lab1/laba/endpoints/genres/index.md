# endpoints/genres.py

Необходимые импорты
```
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlmodel import select, Session
from datetime import datetime

from db.models import Genre, GenreDefault, AppUser
from connection import get_session
from .auth import get_current_user
```
```
router = APIRouter()
```
```
@router.get("/", response_model=list[Genre])
def get_genres(session: Session = Depends(get_session)):
    genres = session.exec(select(Genre)).all()
    return genres
```
```
@router.get("/{genre_id}", response_model=Genre)
def get_genre(genre_id: int, session: Session = Depends(get_session)):
    genre = session.get(Genre, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return genre
```
```
@router.post("/", response_model=Genre)
def create_genre(genre: GenreDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    # Check if the current user is an admin
    print(current_user.is_admin == True)
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin users can create genres")
    
    db_genre = Genre(
        name=genre.name,
    )
    session.add(db_genre)
    session.commit()
    return db_genre
```
```
@router.put("/{genre_id}", response_model=Genre)
def update_genre(genre_id: int, genre: GenreDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin users can update genres")
    
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    # Update the genre's attributes
    db_genre.name = genre.name

    session.add(db_genre)
    session.commit()
    return db_genre
```
```
@router.delete("/{genre_id}")
def delete_genre(genre_id: int, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Only admin users can delete genres")
    
    db_genre = session.get(Genre, genre_id)
    if not db_genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    
    session.delete(db_genre)
    session.commit()
    return {"message": "Genre deleted"}
```