from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

from models.links import CategoryOperationLink


class Category(SQLModel, table=True):  # создаем класс категории и передаем стандартную SQLModel с флагом, что этот класс является таблицей в БД
    id: Optional[int] = Field(default=None, primary_key=True)  # поле с первичным ключом, установлено дефолтно в None для автогенерации
    category: str = Field(unique=True)  # поле с установленым флагом уникальности - записи не смогут повторяться по этому полю
    limit: float = Field(default=0.0)  # поле с дефолтным значением 0
    current: float = Field(default=0.0)
    operations: Optional[List["Operation"]] = Relationship(back_populates="categories",
                                                           link_model=CategoryOperationLink)  # многие-ко-многим
    favourite_category: List["Customer"] = Relationship(back_populates="favourite_category")  # один-ко-многим
    # типы в кавычках, поскольку эти типы есть, но
    # Python интепретируемый язык и не знает, что ниже этой строчки написано или в других файлах
    # + тут будет циклический импорт, что не позволит запустить сервер
    # опциональное (operations) и обязательное (favourite_category) поля, хранящие:
    # список операций со ссылкой на таблицу связи многие-ко-многим
    # список пользователей, у кого эта категория является любимой, со ссылкой на поле в таблице пользователя
    #   back_populates - ссылается на поле "в кавычках" в таблице типа списка
    #   link_model - ссылка на таблицу связи многие-ко-многим
