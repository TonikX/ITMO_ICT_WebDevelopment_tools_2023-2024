=== "Аутентификация"

    ``` py
    import jwt
    import bcrypt
    from fastapi import APIRouter, Depends, HTTPException, Header
    from typing_extensions import Optional
    import os
    from dotenv import load_dotenv, find_dotenv
    from sqlmodel import select
    from datetime import datetime, timedelta
    
    from connection import get_session
    from models import User
    
    
    load_dotenv(find_dotenv('..'))
    secret_key = os.getenv('SECRET_KEY')
    
    
    def hash_password(password: str) -> str:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def verify_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode(), hashed_password.encode())
    
    
    def encode_token(username: str) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(hours=12),
            'iat': datetime.utcnow(),
            'sub': username
        }
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    def decode_token(token: str) -> str:
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid token')
    
    
    router = APIRouter()
    
    
    @router.post("/registration", tags=["auth"])
    def registration(user: User, session=Depends(get_session)) -> dict:
        if user.password is None:
            raise HTTPException(status_code=400, detail='Password must be provided')
    
    
        user.hashed_password = hash_password(user.password)
        user.password = None 
    
        session.add(user)
        session.commit()
        session.refresh(user)
    
        return {"status": 200, "data": user}
    
    
    @router.post("/login", tags=["auth"])
    def login(username: str, password: str, session=Depends(get_session)) -> str:
        query = select(User).where(User.username == username)
        db_user = session.exec(query).one_or_none()
        if not db_user:
            raise HTTPException(status_code=401, detail='Invalid username')
    
        if not verify_password(password, db_user.hashed_password):
            raise HTTPException(status_code=401, detail='Invalid password')
    
        token = encode_token(db_user.username)
        return token
    
    
    @router.get("/user/auth/token", response_model=User, tags=["auth"])
    def get_user_by_token(token: Optional[str] = Header(None), session=Depends(get_session)) -> User:
        if not token:
            raise HTTPException(status_code=401, detail='Unauthorized')
    
        token = token
        user_name = decode_token(token)
        query = select(User).where(User.username == user_name)
        user = session.exec(query).one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    ```
    Описание работы -  Реализовали аутентификацию пользователя с хеширование пароля и JWT токеном

=== "Бюджет"

    ``` py
    
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import Budget
    
    router = APIRouter()
    
    @router.get("/budgets", response_model=List[Budget], tags=["budget"])
    def get_budgets(session=Depends(get_session)) -> List[Budget]:
        return session.exec(select(Budget)).all()
    
    @router.get("/budgets/{budget_id}", response_model=Budget, tags=["budget"])
    def get_budget(budget_id: int, session=Depends(get_session)) -> Budget:
        budget = session.get(Budget, budget_id)
        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")
        return budget
    
    @router.post("/budgets", response_model=Budget, tags=["budget"])
    def create_budget(budget: Budget, session=Depends(get_session)) -> Budget:
        session.add(budget)
        session.commit()
        session.refresh(budget)
        return budget
    
    @router.patch("/budgets/{budget_id}", response_model=Budget, tags=["budget"])
    def update_budget(budget_id: int, budget: Budget, session=Depends(get_session)) -> Budget:
        db_budget = session.get(Budget, budget_id)
        if not db_budget:
            raise HTTPException(status_code=404, detail="Budget not found")
        budget_data = budget.dict(exclude_unset=True)
        for key, value in budget_data.items():
            setattr(db_budget, key, value)
        session.add(db_budget)
        session.commit()
        session.refresh(db_budget)
        return db_budget
    
    @router.delete("/budgets/{budget_id}", tags=["budget"])
    def delete_budget(budget_id: int, session=Depends(get_session)):
        budget = session.get(Budget, budget_id)
        if not budget:
            raise HTTPException(status_code=404, detail="Budget not found")
        session.delete(budget)
        session.commit()
        return {"ok": True}
    ```
    Описание работы -  Реализуем функционал взаимодействий с бюджетом в приложении

=== "Категория трат"

    ``` py
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import Category
    
    router = APIRouter()
    
    @router.get("/categories", response_model=List[Category], tags=["category"])
    def get_categories(session=Depends(get_session)) -> List[Category]:
        return session.exec(select(Category)).all()
    
    @router.get("/categories/{category_id}", response_model=Category, tags=["category"])
    def get_category(category_id: int, session=Depends(get_session)) -> Category:
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category
    
    @router.post("/categories", response_model=Category, tags=["category"])
    def create_category(category: Category, session=Depends(get_session)) -> Category:
        session.add(category)
        session.commit()
        session.refresh(category)
        return category
    
    @router.patch("/categories/{category_id}", response_model=Category, tags=["category"])
    def update_category(category_id: int, category: Category, session=Depends(get_session)) -> Category:
        db_category = session.get(Category, category_id)
        if not db_category:
            raise HTTPException(status_code=404, detail="Category not found")
        category_data = category.dict(exclude_unset=True)
        for key, value in category_data.items():
            setattr(db_category, key, value)
        session.add(db_category)
        session.commit()
        session.refresh(db_category)
        return db_category
    
    @router.delete("/categories/{category_id}", tags=["category"])
    def delete_category(category_id: int, session=Depends(get_session)):
        category = session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        session.delete(category)
        session.commit()
        return {"ok": True}
    ```
    Описание работы -  Реализуем функционал взаимодействий с категориями трат в приложении

=== "Цель"

    ``` py
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import Goal
    
    router = APIRouter()
    
    @router.get("/goals", response_model=List[Goal], tags=["goal"])
    def get_goals(session=Depends(get_session)) -> List[Goal]:
        return session.exec(select(Goal)).all()
    
    @router.get("/goals/{goal_id}", response_model=Goal, tags=["goal"])
    def get_goal(goal_id: int, session=Depends(get_session)) -> Goal:
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        return goal
    
    @router.post("/goals", response_model=Goal, tags=["goal"])
    def create_goal(goal: Goal, session=Depends(get_session)) -> Goal:
        session.add(goal)
        session.commit()
        session.refresh(goal)
        return goal
    
    @router.patch("/goals/{goal_id}", response_model=Goal, tags=["goal"])
    def update_goal(goal_id: int, goal: Goal, session=Depends(get_session)) -> Goal:
        db_goal = session.get(Goal, goal_id)
        if not db_goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        goal_data = goal.dict(exclude_unset=True)
        for key, value in goal_data.items():
            setattr(db_goal, key, value)
        session.add(db_goal)
        session.commit()
        session.refresh(db_goal)
        return db_goal
    
    @router.delete("/goals/{goal_id}", tags=["goal"])
    def delete_goal(goal_id: int, session=Depends(get_session)):
        goal = session.get(Goal, goal_id)
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")
        session.delete(goal)
        session.commit()
        return {"ok": True}
    ```
    Описание работы -  Реализуем функционал взаимодействий с целями накоплений в приложении

=== "Уведомления"

    ``` py
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import Notification
    
    router = APIRouter()
    
    @router.get("/notifications", response_model=List[Notification], tags=["notification"])
    def get_notifications(session=Depends(get_session)) -> List[Notification]:
        return session.exec(select(Notification)).all()
    
    @router.get("/notifications/{notification_id}", response_model=Notification, tags=["notification"])
    def get_notification(notification_id: int, session=Depends(get_session)) -> Notification:
        notification = session.get(Notification, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        return notification
    
    @router.post("/notifications", response_model=Notification, tags=["notification"])
    def create_notification(notification: Notification, session=Depends(get_session)) -> Notification:
        session.add(notification)
        session.commit()
        session.refresh(notification)
        return notification
    
    @router.patch("/notifications/{notification_id}", response_model=Notification, tags=["notification"])
    def update_notification(notification_id: int, notification: Notification, session=Depends(get_session)) -> Notification:
        db_notification = session.get(Notification, notification_id)
        if not db_notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        notification_data = notification.dict(exclude_unset=True)
        for key, value in notification_data.items():
            setattr(db_notification, key, value)
        session.add(db_notification)
        session.commit()
        session.refresh(db_notification)
        return db_notification
    
    @router.delete("/notifications/{notification_id}", tags=["notification"])
    def delete_notification(notification_id: int, session=Depends(get_session)):
        notification = session.get(Notification, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        session.delete(notification)
        session.commit()
        return {"ok": True}

    ```
    Описание работы -  Реализуем функционал уведомлений в приложении

=== "Транзакции"

    ``` py
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import Transaction
    
    router = APIRouter()
    
    @router.get("/transactions", response_model=List[Transaction], tags=["transaction"])
    def get_transactions(session=Depends(get_session)) -> List[Transaction]:
        return session.exec(select(Transaction)).all()
    
    @router.get("/transactions/{transaction_id}", response_model=Transaction, tags=["transaction"])
    def get_transaction(transaction_id: int, session=Depends(get_session)) -> Transaction:
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction
    
    @router.post("/transactions", response_model=Transaction, tags=["transaction"])
    def create_transaction(transaction: Transaction, session=Depends(get_session)) -> Transaction:
        session.add(transaction)
        session.commit()
        session.refresh(transaction)
        return transaction
    
    @router.patch("/transactions/{transaction_id}", response_model=Transaction, tags=["transaction"])
    def update_transaction(transaction_id: int, transaction: Transaction, session=Depends(get_session)) -> Transaction:
        db_transaction = session.get(Transaction, transaction_id)
        if not db_transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        transaction_data = transaction.dict(exclude_unset=True)
        for key, value in transaction_data.items():
            setattr(db_transaction, key, value)
        session.add(db_transaction)
        session.commit()
        session.refresh(db_transaction)
        return db_transaction
    
    @router.delete("/transactions/{transaction_id}", tags=["transaction"])
    def delete_transaction(transaction_id: int, session=Depends(get_session)):
        transaction = session.get(Transaction, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        session.delete(transaction)
        session.commit()
        return {"ok": True}
    ```
    Описание работы -  Реализуем функционал транзакций в приложении

=== "Тип транзакции"

    ``` py
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import TransactionCategory
    
    router = APIRouter()
    
    @router.get("/transaction_categories", response_model=List[TransactionCategory], tags=["transaction_category"])
    def get_transaction_categories(session=Depends(get_session)) -> List[TransactionCategory]:
        return session.exec(select(TransactionCategory)).all()
    
    @router.get("/transaction_categories/{category_id}/{transaction_id}", response_model=TransactionCategory, tags=["transaction_category"])
    def get_transaction_category(category_id: int, transaction_id: int, session=Depends(get_session)) -> TransactionCategory:
        transaction_category = session.get(TransactionCategory, (category_id, transaction_id))
        if not transaction_category:
            raise HTTPException(status_code=404, detail="TransactionCategory not found")
        return transaction_category
    
    @router.post("/transaction_categories", response_model=TransactionCategory, tags=["transaction_category"])
    def create_transaction_category(transaction_category: TransactionCategory, session=Depends(get_session)) -> TransactionCategory:
        session.add(transaction_category)
        session.commit()
        session.refresh(transaction_category)
        return transaction_category
    
    @router.patch("/transaction_categories/{category_id}/{transaction_id}", response_model=TransactionCategory, tags=["transaction_category"])
    def update_transaction_category(category_id: int, transaction_id: int, transaction_category: TransactionCategory, session=Depends(get_session)) -> TransactionCategory:
        db_transaction_category = session.get(TransactionCategory, (category_id, transaction_id))
        if not db_transaction_category:
            raise HTTPException(status_code=404, detail="TransactionCategory not found")
        transaction_category_data = transaction_category.dict(exclude_unset=True)
        for key, value in transaction_category_data.items():
            setattr(db_transaction_category, key, value)
        session.add(db_transaction_category)
        session.commit()
        session.refresh(db_transaction_category)
        return db_transaction_category
    
    @router.delete("/transaction_categories/{category_id}/{transaction_id}", tags=["transaction_category"])
    def delete_transaction_category(category_id: int, transaction_id: int, session=Depends(get_session)):
        transaction_category = session.get(TransactionCategory, (category_id, transaction_id))
        if not transaction_category:
            raise HTTPException(status_code=404, detail="TransactionCategory not found")
        session.delete(transaction_category)
        session.commit()
        return {"ok": True}

    ```
    Описание работы -  реализуем ассоциативную сущность связи транзакций и категории транзакций, для отдельного 
    распределения транзакций на типы

=== "Пользователь"

    ``` py
    from fastapi import APIRouter, Depends, HTTPException
    from typing import List
    from sqlmodel import select
    from connection import get_session
    from models import User
    
    router = APIRouter()
    
    @router.get("/users", response_model=List[User], tags=["user"])
    def get_users(session=Depends(get_session)) -> List[User]:
        return session.exec(select(User)).all()
    
    @router.get("/users/{user_id}", response_model=User, tags=["user"])
    def get_user(user_id: int, session=Depends(get_session)) -> User:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    @router.post("/users", response_model=User, tags=["user"])
    def create_user(user: User, session=Depends(get_session)) -> User:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    @router.patch("/users/{user_id}", response_model=User, tags=["user"])
    def update_user(user_id: int, user: User, session=Depends(get_session)) -> User:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        user_data = user.dict(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
    
    @router.delete("/users/{user_id}", tags=["user"])
    def delete_user(user_id: int, session=Depends(get_session)):
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        session.delete(user)
        session.commit()
        return {"ok": True}

    ```
    Описание работы -  реализуем функционал взаимодействия с пользователем