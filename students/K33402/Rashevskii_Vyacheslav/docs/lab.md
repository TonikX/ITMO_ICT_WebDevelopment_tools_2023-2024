# Lab

## Structure
![structure.png](src%2Fstructure.png)

## Code
### models
```python
from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class CategoryEnum(Enum):
    salary = 'salary'
    home = 'home'
    health = 'health'
    sports = 'sports'
    food = 'food'
    technology = 'technology'
    cashback = 'cashback'
    gifts = 'gifts'
    other = 'other'


class OperationEnum(Enum):
    income = 'income'  # revenue
    outcome = 'outcome'  # expense


class CategoryOperationLink(SQLModel, table=True):  # many-many
    id: Optional[int] = Field(default=None, primary_key=True, unique=True)
    category_id: Optional[int] = Field(
        default=None, foreign_key="category.id", primary_key=True
    )
    operation_id: Optional[int] = Field(
        default=None, foreign_key="operation.id", primary_key=True
    )
    amount: Optional[float] = Field(default=None)


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    category: CategoryEnum = Field(unique=True)
    limit: float = Field(default=0.0)
    current: float = Field(default=0.0)
    operations: Optional[List["Operation"]] = Relationship(back_populates="categories",
                                                           link_model=CategoryOperationLink)  # many-many
    favourite_category: List["Customer"] = Relationship(back_populates="favourite_category")  # 1-many # *


class Operation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    operation: OperationEnum = Field(unique=True)
    limit: float = Field(default=0.0)
    alias: Optional[str] = Field(default=None, nullable=True)
    categories: Optional[List[Category]] = Relationship(back_populates="operations",
                                                        link_model=CategoryOperationLink)  # many-many


class User(SQLModel):
    username: str = Field(unique=True, index=True, nullable=False)
    password: str = Field(nullable=False)
    favourite_category_id: Optional[int] = Field(default=None, foreign_key="category.id")  # 1-many


class Customer(User, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    balance: float = Field(default=0.0, nullable=False)
    favourite_category: Optional[Category] = Relationship(back_populates="favourite_category")  # 1-many # *


class CustomerCategory(User):
    favourite_category: Optional[Category] = None  # *


class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default=None, nullable=False)
    amount: float = Field(default=None, nullable=False)
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")  # 1-many
    category_operation_link_id: Optional[int] = Field(default=None, foreign_key="categoryoperationlink.id")  # 1-many
```

### Customer handler (other are similar)
```python
from typing import List

from fastapi import APIRouter, Depends
from db import get_session
from models import Customer, CustomerCategory

customerRouter = APIRouter(prefix="/customers", tags=["customer"])  # отвечает за swagger


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
    customer = Customer.validate(customer)
    customer.id = None
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@customerRouter.patch("/{username}")
async def update_customer(customer: Customer, username: str, session=Depends(get_session)):
    customer = Customer.validate(customer)
    customer_from_db = session.query(Customer).filter(Customer.username == username).first()
    if customer_from_db is None:
        return "No such customer"
    customer_data = customer.model_dump(exclude_unset=True)
    for key, value in customer_data.items():
        if value is None:
            continue
        setattr(customer_from_db, key, value)
    session.add(customer_from_db)
    session.commit()
    session.refresh(customer_from_db)
    return customer_from_db


@customerRouter.delete("/{username}")
async def delete_customer(username: str, session=Depends(get_session)):
    session.query(Customer).filter(Customer.username == username).delete()
    session.commit()
    return "Deleted"
```

### DB
```python
from sqlmodel import SQLModel, Session, create_engine
from dotenv import load_dotenv
import os

load_dotenv('.env')
db_url = os.getenv('DB_URL')
print(db_url)
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
```

## Screenshots
![get_categories.png](src%2Fget_categories.png)
![get_customers.png](src%2Fget_customers.png)
![patch.png](src%2Fpatch.png)
![post_customer.png](src%2Fpost_customer.png)
## Swagger
![swagger.png](src%2Fswagger.png)