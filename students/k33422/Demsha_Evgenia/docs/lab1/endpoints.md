# Эндпойнты

Эндпойнты для трат:

=== "Создание"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy import cast, Integer
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Expense, ExpenseCategory, Account
    from user_repo.user_endpoints import auth_handler
    
    expense_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/expense_endpoints.py:10:29"
    ```

=== "Получение"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy import cast, Integer
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Expense, ExpenseCategory, Account
    from user_repo.user_endpoints import auth_handler
    
    expense_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/expense_endpoints.py:30:39"
    ```

=== "Изменение"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy import cast, Integer
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Expense, ExpenseCategory, Account
    from user_repo.user_endpoints import auth_handler
    
    expense_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/expense_endpoints.py:39:57"
    ```

=== "Удаление"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy import cast, Integer
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Expense, ExpenseCategory, Account
    from user_repo.user_endpoints import auth_handler
    
    expense_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/expense_endpoints.py:58:"
    ```

Эндпойнты для категорий трат:

=== "Создание"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import ExpenseCategory, CategoryWithExpense
    from user_repo.user_endpoints import auth_handler
    from typing import List
    
    expense_category_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/category_endpoints.py:10:20"
    ```

=== "Получение"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import ExpenseCategory, CategoryWithExpense
    from user_repo.user_endpoints import auth_handler
    from typing import List
    
    expense_category_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])
    
    --8<-- "laboratory_work_1/finance/endpoints/category_endpoints.py:21:29"

    ```

=== "Изменение"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import ExpenseCategory, CategoryWithExpense
    from user_repo.user_endpoints import auth_handler
    from typing import List
    
    expense_category_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/category_endpoints.py:30:43"
    ```

=== "Удаление"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import ExpenseCategory, CategoryWithExpense
    from user_repo.user_endpoints import auth_handler
    from typing import List
    
    expense_category_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/category_endpoints.py:44:"
    ```

Эндпойнты для платежных аккаунтов:

=== "Создание"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Account
    from user_repo.user_endpoints import auth_handler
    
    account_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/account_endpoints.py:9:18"

    ```

=== "Получение"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Account
    from user_repo.user_endpoints import auth_handler
    
    account_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/account_endpoints.py:19:26"
    ```

=== "Изменение"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Account
    from user_repo.user_endpoints import auth_handler
    
    account_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/account_endpoints.py:27:40"
    ```

=== "Удаление"

    ```Python
    from fastapi import APIRouter, Depends, HTTPException
    from sqlalchemy.orm import Session
    from connections import get_session
    from models import Account
    from user_repo.user_endpoints import auth_handler
    
    account_router = APIRouter(dependencies=[Depends(auth_handler.auth_wrapper)])


    --8<-- "laboratory_work_1/finance/endpoints/account_endpoints.py:41:"
    ```
