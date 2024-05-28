# Models for database tables
from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password: str

class Income(BaseModel):
    id: int
    amount: float
    user_id: int
    category_id: int

class Expense(BaseModel):
    id: int
    amount: float
    user_id: int
    category_id: int

class Category(BaseModel):
    id: int
    name: str

class Budget(BaseModel):
    id: int
    amount: float
    category_id: int
    user_id: int

class Report(BaseModel):
    user_id: int
    total_income: float
    total_expense: float
    remaining_budget: float
