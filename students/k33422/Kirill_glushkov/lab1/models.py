from sqlalchemy import Column, DateTime, Float, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from app.database import Base

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    incomes = relationship("IncomeDB", back_populates="user")
    expenses = relationship("ExpenseDB", back_populates="user")
    budgets = relationship("BudgetDB", back_populates="user")

class IncomeDB(Base):
    __tablename__ = 'incomes'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("CategoryDB", back_populates="incomes")
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserDB", back_populates="incomes")

class ExpenseDB(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserDB", back_populates="expenses")
    category = relationship("CategoryDB", back_populates="expenses")


class BudgetDB(Base):
    __tablename__ = 'budgets'

    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
    amount = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("UserDB", back_populates="budgets")
    category = relationship("CategoryDB", back_populates="budgets")

class CategoryDB(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    const = Column(String)
    # Определение связей многие-ко-многим (many-to-many) с другими таблицами
    incomes = relationship("IncomeDB", back_populates="category")
    expenses = relationship("ExpenseDB", back_populates="category")
    budgets = relationship("BudgetDB", back_populates="category")
