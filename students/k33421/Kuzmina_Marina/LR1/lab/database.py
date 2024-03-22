'''from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:123@localhost/itmo"

# Создаем объект базовой модели
Base = declarative_base()

# Определяем модель пользователя
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)

# Создаем таблицы в базе данных
Base.metadata.create_all(bind=engine)

# Создаем функцию для создания сессии базы данных
def get_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

# Функция для получения пользователя из базы данных по ID
def get_user(user_id: int, session):
    return session.query(User).filter(User.id == user_id).first()

# Функция для получения пользователя из базы данных по имени пользователя
def get_user_by_username(username: str, session):
    return session.query(User).filter(User.username == username).first()

# Функция для создания нового пользователя в базе данных
def create_user(user_data: dict, session):
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

# Функция для обновления информации о пользователе в базе данных
def update_user(user_id: int, user_data: dict, session):
    user = get_user(user_id, session)
    if user:
        for key, value in user_data.items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
    return user

# Функция для удаления пользователя из базы данных
def delete_user(user_id: int, session):
    user = get_user(user_id, session)
    if user:
        session.delete(user)
        session.commit()
    return user

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # Определение связей один-ко-многим (one-to-many) с другими таблицами
    incomes = relationship("Income", back_populates="owner")
    expenses = relationship("Expense", back_populates="owner")

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Определение связей один-ко-многим (one-to-many) с другими таблицами
    owner = relationship("User", back_populates="incomes")
    category = relationship("Category", back_populates="incomes")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    category_id = Column(Integer, ForeignKey("categories.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Определение связей один-ко-многим (one-to-many) с другими таблицами
    owner = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Определение связей многие-ко-многим (many-to-many) с другими таблицами
    incomes = relationship("Income", back_populates="category")
    expenses = relationship("Expense", back_populates="category")

'''