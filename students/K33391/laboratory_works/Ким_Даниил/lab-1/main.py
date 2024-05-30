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


# Endpoints for Budget CRUD operations
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


# Endpoints for Income CRUD operations
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


# Endpoints for Expense CRUD operations
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



@app.get("/financial-report/{user_id}", response_model=dict)
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


@app.get("/budget-notifications/{user_id}", response_model=list)
def budget_notifications(user_id: int, db: Session = Depends(get_db)):
    # Получаем пользователя
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    notifications = []

    # Проходим по всем бюджетам пользователя
    for budget in user.budgets:
        # Считаем общие расходы по текущему бюджету
        total_expenses = sum(expense.amount for expense in budget.category.expenses)

        # Если общие расходы превышают установленный лимит
        if total_expenses > budget.amount:
            notification = {
                "budget_id": budget.id,
                "category_name": budget.category.name,
                "total_expenses": total_expenses,
                "budget_amount": budget.amount
            }
            notifications.append(notification)

    return notifications