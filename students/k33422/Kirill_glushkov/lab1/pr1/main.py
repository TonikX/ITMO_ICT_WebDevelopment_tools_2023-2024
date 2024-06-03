from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
import uvicorn
from datetime import datetime
from app.database import SessionLocal
from app.models import Budget, Expense, Income, User
from sqlalchemy import and_, func


temp_bd = [
    User(id=1, name="Мартынов Дмитрий", incomes=[Income(date='2024-05-28', amount=1000.0, category='salary'), Income(date='2024-06-01', amount=500.0, category='bonus')], 
         expenses=[Expense(date='2024-05-28', amount=500.0, category='rent'), Expense(date='2024-06-01', amount=200.0, category='food')], 
         budgets=[Budget(category='rent', amount=1000.0), Budget(category='food', amount=500.0)]),
    User(id=2, name="Петров Иван", incomes=[Income(date='2024-05-29', amount=800.0, category='salary'), Income(date='2024-06-02', amount=300.0, category='bonus')], 
         expenses=[Expense(date='2024-05-29', amount=300.0, category='rent'), Expense(date='2024-06-02', amount=150.0, category='food')], 
         budgets=[Budget(category='rent', amount=800.0), Budget(category='food', amount=300.0)]),
    User(id=3, name="Сидоров Сергей", incomes=[Income(date='2024-05-30', amount=1200.0, category='salary'), Income(date='2024-06-03', amount=400.0, category='bonus')], 
         expenses=[Expense(date='2024-05-30', amount=400.0, category='rent'), Expense(date='2024-06-03', amount=200.0, category='food')], 
         budgets=[Budget(category='rent', amount=1200.0), Budget(category='food', amount=400.0)]),
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.on_event("startup")
def startup():
    with SessionLocal() as session:
        session.execute("SELECT 1")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/temp_db")
async def get_temp_db():
    return temp_bd

@app.delete("/temp_db/{user_id}")
async def delete_user(user_id: int):
    for user in temp_bd:
        if user["id"] == user_id:
            temp_bd.remove(user)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/temp_db/{user_id}")
async def update_user(user_id: int, user: User):
    for user_db in temp_bd:
        if user_db["id"] == user_id:
            user_db["name"] = user.name
            user_db["incomes"] = user.incomes
            user_db["expenses"] = user.expenses
            user_db["budgets"] = user.budgets
            return {"id": user_id, "name": user.name, "incomes": user.incomes, "expenses": user.expenses, "budgets": user.budgets}
    raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True, workers=1, log_level='debug', access_log=True)