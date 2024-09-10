# Lab

## Structure
![structure.png](src%2Fstructure.png)

## Code
### models
```python
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime


class CategoryOperationLink(SQLModel, table=True):  # многие-ко-многим, связь категорий и операций
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    category_id: Optional[int] = Field(default=None,
                                       foreign_key="category.id", primary_key=True)  # внешний ключ
    operation_id: Optional[int] = Field(default=None,
                                        foreign_key="operation.id", primary_key=True)  # внешний ключ


class Category(SQLModel, table=True):
    # поле с первичным ключом, установлено дефолтно в None для автогенерации
    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(unique=True)
    limit: float = Field(default=0.0)
    current: float = Field(default=0.0)
    operations: Optional[List["Operation"]] = Relationship(back_populates="categories",
                                                           link_model=CategoryOperationLink)  # многие-ко-многим
    favourite_category: List["Customer"] = Relationship(back_populates="favourite_category")  # один-ко-многим
    # типы в кавычках, поскольку эти типы есть, но
    # Python интепретируемый язык и не знает, что ниже этой строчки написано или в других файлах
    # опциональное (operations) и обязательное (favourite_category) поля, хранящие:
    # список операций со ссылкой на таблицу связи многие-ко-многим
    # список пользователей, у кого эта категория является любимой, со ссылкой на поле в таблице пользователя
    #   back_populates - ссылается на поле "в кавычках" в таблице типа списка
    #   link_model - ссылка на таблицу связи многие-ко-многим


class User(SQLModel):
    username: str = Field(unique=True, index=True, nullable=False)
    password: str = Field(nullable=False)
    favourite_category_id: Optional[int] = Field(default=None, foreign_key="category.id")  # один-ко-многим


class Customer(User, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: float = Field(default=0.0, nullable=False)
    favourite_category: Optional[Category] = Relationship(back_populates="favourite_category")
    # один-ко-многим, один пользователь может иметь одну любимую категорию, но одну категорию может выбрать множество пользлователей


class CustomerCategory(User):
    # класс наследник от дефолтного пользователя - служит для отображения категории целиком дополнительно к id
    favourite_category: Optional[Category] = None


class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    operation: str = Field(unique=True)
    limit: float = Field(default=0.0)
    alias: Optional[str] = Field(default=None, nullable=True)
    categories: Optional[List[Category]] = Relationship(back_populates="operations",
                                                        link_model=CategoryOperationLink)  # многие-ко-многим


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default=None, nullable=False)  # тип данных дата и время
    amount: float = Field(default=None, nullable=False)
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")  # один-ко-многим
    category_operation_link_id: Optional[int] = Field(default=None,
                                                      foreign_key="categoryoperationlink.id")  # один-ко-многим

```

### Customer handler (other are similar)
```python
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from db import get_session
from models.models import Customer, CustomerCategory

customerRouter = APIRouter(prefix="/customers", tags=["Пользователь"])  # tags отвечает за swagger


@customerRouter.get("/", response_model=list[CustomerCategory])
async def get_customers(session=Depends(get_session)) -> List[Customer]:
    customers = session.query(Customer).all()
    return customers


@customerRouter.get("/{username_id}", response_model=CustomerCategory)
async def get_customer(username_id: int, session=Depends(get_session)) -> Customer:
    customer = session.get(Customer, username_id)
    return customer


@customerRouter.post("/")
async def create_customer(customer: Customer, session=Depends(get_session)):
    customer.id = None
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@customerRouter.patch("/{username_id}")
async def update_customer(customer: Customer, username_id: int, session=Depends(get_session)):
    customer_from_db = session.query(Customer).filter_by(id=username_id).first()
    if customer_from_db is None:  # если запись с переданным id не найдена, то возвращаем исключение
        raise HTTPException(status_code=404, detail="No such customer")
    customer_data = customer.model_dump(exclude_unset=True)
    for key, value in customer_data.items():
        if value is None:
            continue
        setattr(customer_from_db, key, value)
    session.add(customer_from_db)
    session.commit()
    session.refresh(customer_from_db)
    return customer_from_db


@customerRouter.delete("/{username_id}")
async def delete_customer(username_id: int, session=Depends(get_session)):
    session.query(Customer).filter_by(id=username_id).delete()
    session.commit()
    return "Deleted"
```

## Screenshots
![get_categories.png](src%2Fget_categories.png)
![get_customers.png](src%2Fget_customers.png)
![patch.png](src%2Fpatch.png)
## Swagger
![swagger.png](src%2Fswagger.png)