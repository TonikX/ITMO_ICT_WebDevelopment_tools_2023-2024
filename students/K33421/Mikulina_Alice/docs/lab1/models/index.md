# models.py

Необходимые импорты
```
from enum import Enum
from typing import List, Optional
from datetime import datetime
from sqlmodel import Field, Relationship, SQLModel
```

Классы AppUserDefault и AppUser. Эти классы определяют информацию о пользователе, включая имя пользователя, адрес электронной почты, пароль, информацию о себе и местоположение. Класс AppUser наследует от AppUserDefault и добавляет дополнительные поля, такие как id, is_admin, Create_at и Last_updated_at.
```
class AppUserDefault(SQLModel):
    username: str
    email: str
    password: str
    about: Optional[str] = None
    location: Optional[str] = None

class AppUser(AppUserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    is_admin: Optional[bool] = Field(default=False)
    created_at: Optional[str] = Field(default_factory=datetime.now)
    last_updated_at: Optional[str] = Field(default_factory=datetime.now)
```

Классы BookGenreDefault и BookGenre. Эти классы определяют взаимосвязь между книгами и жанрами. Класс BookGenre наследует от BookGenreDefault и добавляет поле id.
```
class BookGenreDefault(SQLModel):
    book_id: int = Field(foreign_key="book.id")
    genre_id: int = Field(foreign_key="genre.id")

class BookGenre(BookGenreDefault, table=True):
    id: int = Field(default=None, primary_key=True)
```

Классы GenreDefault и Genre. Эти классы определяют информацию о жанре, включая название. Класс Genre наследует от GenreDefault и имеет связь с классом Book.
```
class GenreDefault(SQLModel):
    name: str

class Genre(GenreDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    books: Optional[List["Book"]] = Relationship(
        back_populates="genres",
        link_model=BookGenre
    )
```

Классы BookDefault и Book. Эти классы определяют информацию о книге, включая название, автора, описание и состояние. Класс Book наследует от BookDefault и добавляет такие поля, как id, user_id, Create_at и Last_updated_at, а также связь с классом Genre.
```
class BookDefault(SQLModel):
    title: str
    author: str
    description: Optional[str] = None
    condition: str

class Book(BookDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="appuser.id")
    created_at: Optional[str] = Field(default_factory=datetime.now)
    last_updated_at: Optional[str] = Field(default_factory=datetime.now)
    genres: Optional[List[Genre]] = Relationship(
        back_populates="books",
        link_model=BookGenre
    )
```

Перечисление StatusType: это перечисление определяет возможные статусы запроса на обмен книг, включая «ожидание», «отклонено», «одобрено» и «обменено».
```
class StatusType(Enum):
    pending = "pending"
    declined = "declined"
    approved = "approved"
    exchanged = "exchanged"
```

Классы RequestDefault и Request: эти классы определяют информацию запроса на обмен книгами, включая идентификатор книги запрашивающего, идентификатор книги получателя, сообщение и статус. Класс Request наследует от RequestDefault и добавляет поля id, Create_at и Last_updated_at.
```
class RequestDefault(SQLModel):
    requester_book_id: int = Field(foreign_key="book.id")
    recipient_book_id: int = Field(foreign_key="book.id")
    message: str
    status: StatusType

class Request(RequestDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default_factory=datetime.now)
    last_updated_at: Optional[str] = Field(default_factory=datetime.now)
```