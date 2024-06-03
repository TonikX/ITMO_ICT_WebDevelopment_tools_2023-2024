from typing import List
from pydantic import BaseModel
from bcrypt import hashpw, gensalt

from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str
    email: str

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

