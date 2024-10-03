# Лабораторная работа № 1

## Задание
### Разработка сервиса для управления личными финансами
Необходимо создать простой сервис для управления личными финансами. Сервис должен позволять пользователям вводить доходы и расходы, устанавливать бюджеты на различные категории, а также просматривать отчеты о своих финансах. Дополнительные функции могут включать в себя возможность получения уведомлений о превышении бюджета, анализа трат и установки целей на будущее.

## Процесс разработки

`db.py`
```python
from sqlmodel import SQLModel, Session, create_engine

db_url = 'postgresql://postgres:postgres@localhost/lab_db'
engine = create_engine(db_url, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
```
`main.py`
```python

from fastapi import FastAPI, Depends, HTTPException

from models import *
from db import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users", response_model=List[User])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.post("/user")
def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.delete("/user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted successfully"}


@app.patch("/user/{user_id}")
def update_user(user_id: int, user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user.dict().items():
        setattr(db_user, attr, value)
    db.commit()
    db.refresh(db_user)
    return db_user


# Endpoints for Budget
@app.get("/budget/{budget_id}", response_model=Budget)
def get_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget


@app.get("/budgets", response_model=List[Budget])
def get_budgets(db: Session = Depends(get_db)):
    return db.query(Budget).all()


@app.post("/budget")
def create_budget(budget: BudgetBase, db: Session = Depends(get_db)):
    db_budget = Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@app.delete("/budget/{budget_id}")
def delete_budget(budget_id: int, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    db.delete(db_budget)
    db.commit()
    return {"message": "Budget deleted successfully"}


@app.patch("/budget/{budget_id}")
def update_budget(budget_id: int, budget: BudgetBase, db: Session = Depends(get_db)):
    db_budget = db.query(Budget).filter(Budget.id == budget_id).first()
    if not db_budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    for attr, value in budget.dict().items():
        setattr(db_budget, attr, value)
    db.commit()
    db.refresh(db_budget)
    return db_budget


# Endpoints for Category CRUD operations
@app.get("/category/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@app.get("/categories", response_model=List[Category])
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.post("/category")
def create_category(category: CategoryBase, db: Session = Depends(get_db)):
    db_category = Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@app.delete("/category/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}


@app.patch("/category/{category_id}")
def update_category(category_id: int, category: CategoryBase, db: Session = Depends(get_db)):
    db_category = db.query(Category).filter(Category.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for attr, value in category.dict().items():
        setattr(db_category, attr, value)
    db.commit()
    db.refresh(db_category)
    return db_category


# Endpoints for Incomes
@app.get("/income/{income_id}", response_model=Income)
def get_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(Income).filter(Income.id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    return db_income


@app.get("/incomes", response_model=List[Income])
def get_incomes(db: Session = Depends(get_db)):
    return db.query(Income).all()


@app.post("/income")
def create_income(income: IncomeBase, db: Session = Depends(get_db)):
    db_income = Income(**income.dict())
    db.add(db_income)
    db.commit()
    db.refresh(db_income)
    return db_income


@app.delete("/income/{income_id}")
def delete_income(income_id: int, db: Session = Depends(get_db)):
    db_income = db.query(Income).filter(Income.id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    db.delete(db_income)
    db.commit()
    return {"message": "Income deleted successfully"}


@app.patch("/income/{income_id}")
def update_income(income_id: int, income: IncomeBase, db: Session = Depends(get_db)):
    db_income = db.query(Income).filter(Income.id == income_id).first()
    if not db_income:
        raise HTTPException(status_code=404, detail="Income not found")
    for attr, value in income.dict().items():
        setattr(db_income, attr, value)
    db.commit()
    db.refresh(db_income)
    return db_income


# Endpoints for Expense
@app.get("/expense/{expense_id}", response_model=Expense)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense


@app.get("/expenses", response_model=List[Expense])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


@app.post("/expense")
def create_expense(expense: ExpenseBase, db: Session = Depends(get_db)):
    db_expense = Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/expense/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


@app.patch("/expense/{expense_id}")
def update_expense(expense_id: int, expense: ExpenseBase, db: Session = Depends(get_db)):
    db_expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    for attr, value in expense.dict().items():
        setattr(db_expense, attr, value)
    db.commit()
    db.refresh(db_expense)
    return db_expense


#https://www.figma.com/design/GKc6sROqiDpg0Ht82MzHf1/Finance-Tracker?node-id=0-1&node-type=canvas&t=q1L0quBhVY17c4TW-0
# Нужен для главной страницы, чтобы клиент не вычислял это у себя на стороне. см фигму главный экран
@app.get("/report/{user_id}", response_model=dict)
def financial_report(user_id: int, db: Session = Depends(get_db)):
    # Получаем пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}

    # Считаем общий баланс
    total_balance = sum(income.amount for income in user.incomes) - sum(expense.amount for expense in user.expenses)

    # Получаем список доходов пользователя
    user_incomes = [income.dict() for income in user.incomes]

    # Получаем список расходов пользователя
    user_expenses = [expense.dict() for expense in user.expenses]

    # Получаем список бюджетов пользователя
    user_budgets = [budget.dict() for budget in user.budgets]

    return {
        "user_id": user.id,
        "total_balance": total_balance,
        "incomes": user_incomes,
        "expenses": user_expenses,
        "budgets": user_budgets
    }


# Firebase пуши на мобилку
@app.get("/notifications/{user_id}", response_model=list)
def budget_notifications(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    notifications = []

    for budget in user.budgets:
        total_expenses = sum(expense.amount for expense in budget.category.expenses)

        if total_expenses > budget.amount:
            notification = {
                "budget_id": budget.id,
                "category_name": budget.category.name,
                "total_expenses": total_expenses,
                "budget_amount": budget.amount
            }
            notifications.append(notification)

    return notifications
```

```python
from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    username: str
    email: str
    password: str


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)
    categories: List["Category"] = Relationship(back_populates="user")
    incomes: List["Income"] = Relationship(back_populates="user")
    expenses: List["Expense"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")


class CategoryBase(SQLModel):
    name: str
    description: str
    user_id: int = Field(foreign_key="user.id")


class Category(CategoryBase, table=True):
    id: int = Field(default=None, primary_key=True)
    incomes: List["Income"] = Relationship(back_populates="category")
    expenses: List["Expense"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(back_populates="category")
    user: User = Relationship(back_populates="categories")


class IncomeBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Income(IncomeBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="incomes")
    category: Category = Relationship(back_populates="incomes")


class ExpenseBase(SQLModel):
    amount: float
    description: str
    date: datetime = Field(default=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Expense(ExpenseBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="expenses")
    category: Category = Relationship(back_populates="expenses")


class BudgetBase(SQLModel):
    amount: float
    date_valid_until: datetime
    user_id: int = Field(foreign_key="user.id")
    category_id: int = Field(foreign_key="category.id")


class Budget(BudgetBase, table=True):
    id: int = Field(default=None, primary_key=True)
    user: User = Relationship(back_populates="budgets")
    category: Category = Relationship(back_populates="budgets")

```

# Выводы

Создал интерфейс для сервиса бюджета, который буду интегрировать в приложение на андроиде
