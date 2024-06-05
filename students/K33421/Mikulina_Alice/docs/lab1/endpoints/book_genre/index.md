# endpoints/book_genre.py

Необходимые импорты
```
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlmodel import select, Session
from datetime import datetime

from db.models import BookGenre, BookGenreDefault, AppUser, Book, Genre
from connection import get_session
from .auth import get_current_user
```

Маршрутизатор. Код создает экземпляр APIRouter с именем router.
```
router = APIRouter()
```

GET "/": получить все BookGenres: функция get_booksgenres извлекает все объекты BookGenre из базы данных, используя функцию выбора из SQLModel и функцию get_session для получения сеанса базы данных.
```
@router.get("/", response_model=list[BookGenre])
def get_booksgenres(session: Session = Depends(get_session)):
    books_genres = session.exec(select(BookGenre)).all()
    return books_genres
```

GET "/{book_genre_id}": получение определенного BookGenre: функция get_bookgenre извлекает конкретный объект BookGenre из базы данных на основе параметра book_genre_id. Если BookGenre не найден, он вызывает исключение HTTPException с кодом состояния 404.
```
@router.get("/{book_genre_id}", response_model=BookGenre)
def get_bookgenre(book_genre_id: int, session: Session = Depends(get_session)):
    book_genre = session.get(BookGenre, book_genre_id)
    if not book_genre:
        raise HTTPException(status_code=404, detail="BookGenre not found")
    return book_genre
```

POST «/»: создать новый BookGenre: функция create_bookgenre создает новый объект BookGenre в базе данных. В качестве входных данных он принимает объект BookGenreDefault, который представляет собой pydantic модель, представляющую данные, необходимые для создания нового BookGenre. Функция также извлекает соответствующие объекты «Книга» и «Жанр» из базы данных, обновляет их связи и сохраняет изменения в базе данных.
```
@router.post("/", response_model=BookGenre)
def create_bookgenre(book_genre: BookGenreDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    print(book_genre.book_id)
    db_book_genre = BookGenre(
        book_id=book_genre.book_id,
        genre_id=book_genre.genre_id,
    )

    db_book = session.get(Book, db_book_genre.book_id)
    db_genre = session.get(Genre, db_book_genre.genre_id)

    db_book.genres.append(db_genre)
    db_genre.books.append(db_book)

    session.add(db_book)
    session.add(db_genre)
    session.add(db_book_genre)
    session.commit()
    return db_book_genre
```

PUT «/{book_genre_id}»: обновить BookGenre: функция update_bookgenre обновляет существующий объект BookGenre в базе данных. Параметр book_genre_id используется для идентификации обновляемого BookGenre, а объект BookGenreDefault — для обновления полей book_id и жанр_id.
```
@router.put("/{book_genre_id}", response_model=BookGenre)
def update_bookgenre(book_genre_id: int, book_genre: BookGenreDefault, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book_genre = session.get(BookGenre, book_genre_id)
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="BookGenre not found")
    
    # Update the book_genre's attributes
    db_book_genre.book_id = book_genre.book_id
    db_book_genre.genre_id = book_genre.genre_id

    session.add(db_book_genre)
    session.commit()
    return db_book_genre
```

DELETE «/{book_genre_id}»: удаление BookGenre: функция delete_bookgenre удаляет существующий объект BookGenre из базы данных на основе параметра book_genre_id. Если BookGenre не найден, он вызывает исключение HTTPException с кодом состояния 404.
```
@router.delete("/{book_genre_id}")
def delete_bookgenre(book_genre_id: int, session: Session = Depends(get_session), current_user: AppUser = Depends(get_current_user)):
    db_book_genre = session.get(BookGenre, book_genre_id)
    if not db_book_genre:
        raise HTTPException(status_code=404, detail="BookGenre not found")
    
    session.delete(db_book_genre)
    session.commit()
    return {"message": "BookGenre deleted"}
```