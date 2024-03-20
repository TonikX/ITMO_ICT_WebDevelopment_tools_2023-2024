from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class Genre(str, Enum):
    Fiction = "fiction"
    NonFiction = "non-fiction"
    Mystery = "mystery"
    Romance = "romance"
    ScienceFiction = "science-fiction"


class Author(BaseModel):
    id: int
    name: str
    bio: Optional[str]


# Модель данных для профиля пользователя
class UserProfile(BaseModel):
    id: int
    username: str
    firstname: Optional[str]
    lastname: Optional[str]
    age: int
    location: Optional[str]
    bio: Optional[str]


# Модель данных для книги
class Book(BaseModel):
    id: int
    title: str
    author_id: Author
    genre: Genre
    bio: Optional[str]


# Модель данных для библиотеки пользователя
class UserLibrary(BaseModel):
    id: int
    user_id: UserProfile
    books: List[Book] = []  # Книги в библиотеке пользователя


# Модель данных для запроса на обмен
class ExchangeRequest(BaseModel):
    id: int
    requester_id: str  # Юзернэйм пользователя, предложившего обмен
    recipient_id: str  # Юзернэйм пользователя, получившего запрос на обмен
    book_offered_id: List[int] = []  # Список ID книг, предложенных для обмена
    book_requested_id: List[int] = []  # Список ID книг, запрошенных для обмена
    accepted: bool  # Статус запроса (принят или отклонен)


# Модель данных для отзывов о пользователе
class UserReview(BaseModel):
    id: int
    reviewer_id: UserProfile  # Пользователь, оставивший отзыв
    reviewed_id: UserProfile  # Пользователь, оцененный в отзыве
    rating: int  # Оценка пользователя
    review_text: Optional[str]  # Текст отзыва


# Модель данных для отзывов о книге
class BookReview(BaseModel):
    id: int
    book_id: Book  # Ссылка на книгу, о которой оставлен отзыв
    reviewer_id: UserProfile  # Ссылка на профиль пользователя, оставившего отзыв
    rating: int  # Оценка книги
    review_text: Optional[str]  # Текст отзыва
