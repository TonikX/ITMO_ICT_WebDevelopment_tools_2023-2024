# Лабораторная работа 1
## Практические работы

- [Практическая работа 1](./practical_work_1)
- [Практическая работа 2](./practical_work_2)
- [Практическая работа 3](./practical_work_3)

## Задание
Разработайте простую программу-тайм-менеджер, которая поможет управлять вашим временем и задачами. Программа должна позволять создавать задачи с описанием, устанавливать им сроки выполнения и приоритеты, а также отслеживать затраченное время на каждую задачу.
## Структура проекта
```
lr1
├── alembic.ini
├── conn.py
├── dependencies
│   ├── __init__.py
│   └── auth.py
├── main.py
├── migrations
│   ├── README
│   ├── env.py
│   ├── script.py.mako
│   └── versions
│       └── 098f28c3e810_.py
├── models.py
└── routers
    ├── __init__.py
    ├── auth
    │   ├── __init__.py
    │   ├── models.py
    │   └── router.py
    ├── budgets
    │   ├── __init__.py
    │   ├── models.py
    │   └── router.py
    ├── budgets_in_categories
    │   ├── __init__.py
    │   └── router.py
    ├── categories
    │   ├── __init__.py
    │   ├── models.py
    │   └── router.py
    ├── transactions
    │   ├── __init__.py
    │   ├── models.py
    │   └── router.py
    └── users
        ├── __init__.py
        ├── models.py
        └── router.py
```

## Модели данных

Для описания таблиц воспользуемся библиотекой `sqlmodel`.

Создадим сущность пользователя со следующими полями:

```python
class User(SQLModel, table=True):
    __tablename__ = "users"
    user_id: int = Field(primary_key=True)
    username: str
    email: str
    password_hash: str
```

Далее, создадим таблицу для хранения транзакций. У данной таблицы будет связь с пользователем и категорией трат
```python
class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    transaction_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    amount: float
    transaction_type: str
    category_id: int = Field(foreign_key="categories.category_id")
    timestamp: datetime.datetime

    user: User = Relationship()
    category: "Category" = Relationship(back_populates="transactions")
```

Создадим таблицу, необходимую для связи бюджета и категории
```python
class BudgetCategoryLink(SQLModel, table=True):
    __tablename__ = "budgets_categories"

    budget_id: int = Field(primary_key=True, foreign_key="budgets.budget_id")
    category_id: int = Field(primary_key=True, foreign_key="categories.category_id")
```

Создадим таблицу для хранения бюджета, установленного пользователем. Можно будет указать период и сумму трат
```python
class Budget(SQLModel, table=True):
    __tablename__ = "budgets"
    budget_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    amount: float
    period_start: datetime.datetime
    period_end: datetime.datetime
```

У пользователей будет возможность категоризации трат. Для этого создадим отдельную таблицу. Связь с бюджетами реализуем при помощи таблицы `BudgetCategoryLink`
```python
class Category(SQLModel, table=True):
    __tablename__ = "categories"
    category_id: int = Field(primary_key=True)
    category_name: str
    transactions: List[Transaction] = Relationship(back_populates="category")
    budgets: Optional[list[Budget]] = Relationship(link_model=BudgetCategoryLink)
```

Также создадим вспомогательные таблицы для нотификаций, анализа трат и установки целей
```python
class BudgetExceedNotification(SQLModel, table=True):
    __tablename__ = "budgetexceednotification"
    notification_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    budget_id: int = Field(foreign_key="budgets.budget_id")
    threshold_amount: float
    timestamp: datetime.datetime


class SpendingAnalysis(SQLModel, table=True):
    __tablename__ = "spendinganalysis"
    analysis_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    category_id: int = Field(foreign_key="categories.category_id")
    total_spent: float
    timestamp: datetime.datetime


class FinancialGoal(SQLModel, table=True):
    __tablename__ = "financialgoals"
    goal_id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.user_id")
    goal_name: str
    target_amount: float
    current_amount: float
    target_date: datetime.datetime
```

## API

### Пользователи
На примере пользователя покажем код для реализации CRUD endpoint'ов для модели данных

Для разделения логики воспользуемся классом `APIRouter`, который мы затем подключим к нашему приложению. При инициализации передадим префикс `/users/` для того, чтобы в дальнейшем его не указывать.
```python
router = APIRouter(prefix="/users")
```

Далее представлены модели pydantic, которые будут использованы для ответов сервера и получения данных
```python
from typing import TypedDict

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserRead(BaseModel):
    user_id: int
    username: str
    email: str


class UserUpdate(BaseModel):
    username: str
    email: str


class DeletedUserResponse(TypedDict):
    message: str
```

На POST запрос создадим пользователя с параметрами, переданными в запросе. Пароль будем хешировать при помощи функции sha512
```python
@router.post("", response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)) -> User:
    user_obj = User(**user.model_dump(), password_hash=sha512(user.password.encode()).hexdigest())
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj
```

Получение пользователя достаточно тривиально, нужно лишь воспользоваться методом `get` у объекта сессии
```python
@router.get("/{user_id}", response_model=UserRead, dependencies=[Depends(verify_jwt)])
def get_user(user_id: int, session: Session = Depends(get_session)) -> User:
    if (user := session.get(User, user_id)) is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user
```

Получить список всех пользователей можно при помощи метода `exec`
```python
@router.get("", dependencies=[Depends(verify_jwt)])
def list_users(session: Session = Depends(get_session)) -> list[User]:
    return session.exec(select(User)).all()
```

Обновим данные пользователя на PUT запрос
```python
@router.put("/{user_id}", response_model=UserRead, dependencies=[Depends(verify_jwt)])
def update_user(user_id: int, user: UserUpdate, session: Session = Depends(get_session)) -> User:
    user_obj = session.get(User, user_id)
    if not user_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    user_obj.sqlmodel_update(user.model_dump(exclude_unset=True))
    session.add(user_obj)
    session.commit()
    session.refresh(user_obj)
    return user_obj
```

Удалим пользователя на DELETE запрос
```python
@router.delete("/{user_id}", dependencies=[Depends(verify_jwt)])
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_obj = session.get(User, user_id)
    if not user_obj:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    session.delete(user_obj)
    session.commit()
    return {"message": "User deleted successfully"}
```

### JWT

Авторизацию запросов при помощи JWT токена можно реализовать достаточно легко

Создадим функцию, которая будет из headers запроса доставать необходимые ключ и проверять его подлинность

```python
import os
from http import HTTPStatus
import jwt
from fastapi import HTTPException, Request

def verify_jwt(request: Request):
    try:
        return jwt.decode(request.headers.get("authorization", "").split()[-1], os.getenv("JWT_KEY"), ["HS256"])
    except (jwt.exceptions.PyJWTError, IndexError):
        raise HTTPException(HTTPStatus.UNAUTHORIZED)

```

Затем создадим endpoint для генерации токена

В нем получим пользователя, которые запрашивает токен, сравним его пароль с тем, которые есть в базе и создадим токен

```python
router = APIRouter(prefix="/auth")

@router.post("")
def generate_token(data: TokenCreate, session: Session = Depends(get_session)) -> TokenCreateResponse:
    if (user := session.exec(select(User).where(User.email == data.email)).one()) is None:
        raise HTTPException(HTTPStatus.NOT_FOUND, "User was not found")
    if not hmac.compare_digest(sha512(data.password.encode()).digest(), unhexlify(user.password_hash.encode())):
        raise HTTPException(HTTPStatus.UNAUTHORIZED)
    iat = datetime.now(tz=timezone.utc)
    return {
        "token": jwt.encode(
            {"sub": data.email, "exp": int((iat + timedelta(minutes=15)).timestamp()), "iat": int(iat.timestamp())},
            os.getenv("JWT_KEY"),
        )
    }
```

Затем в остальных роутерах укажем функцию verify_jwt, как зависимость. Она будет вызываться перед обработкой каждого запроса

```python
router = APIRouter(prefix="/transactions", dependencies=[Depends(verify_jwt)])
```

## Миграции
Настроим миграции при помощи библиотеки alembic

```sh
alembic init migrations
alembic upgrade head
```