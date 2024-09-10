from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

from models.categories import Category


class User(SQLModel): # создаем класс пользователя и передаем стандартную SQLModel без флага таблицы
    username: str = Field(unique=True, index=True, nullable=False)  # поле уникальное недопускающее null значения и по которому строится индекс
    password: str = Field(nullable=False)
    favourite_category_id: Optional[int] = Field(default=None, foreign_key="category.id")  # один-ко-многим, опциональное поле с внешним ключом к category.id


class Customer(User, table=True): # создаем класс потребителя на основе пользователя и передаем флаг таблицы - будет содержать свои поля и поля пользователя
    id: Optional[int] = Field(default=None, primary_key=True)  # поле с первичным ключом
    balance: float = Field(default=0.0, nullable=False)
    favourite_category: Optional[Category] = Relationship(back_populates="favourite_category")  # один-ко-многим, один пользователь может иметь одну любимую категорию, но одну категорию может выбрать множество пользлователей


class CustomerCategory(User):  # класс наследник от дефолтного пользователя - служит для отображения категории целиком дополнительно к id
    favourite_category: Optional[Category] = None
