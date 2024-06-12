# Пользователь

Модели для пользователя, которые окажутся в базе данных или будут формами для регистрации, входа и смены пароля:

=== "Модель пользователя"

    ```Python
    from sqlmodel import SQLModel, Field, Relationship


    --8<-- "laboratory_work_1/finance/user_repo/user_models.py:11:24"
    ```

=== "Модели для регистрации и аутентификации"

    ```Python
    from sqlmodel import SQLModel, Field, Relationship
    from pydantic import field_validator, EmailStr


    --8<-- "laboratory_work_1/finance/user_repo/user_models.py:25:42"
    ```

=== "Модель для смены пароля"

    ```Python
    from sqlmodel import SQLModel, Field, Relationship
    from pydantic import field_validator, EmailStr


    --8<-- "laboratory_work_1/finance/user_repo/user_models.py:43:54"
    ```


В этом классе (обработчике) предоставляет методы, с помощью которых
реализуется авторизация, регистрация, генерация JWT-токенов, аутентификация по JWT-токену,
хэширование паролей:

=== "Создание класса"

    ```Python
    --8<-- "laboratory_work_1/finance/user_repo/auth.py::14"
    ```

=== "Обработка пароля"

    ```Python
    --8<-- "laboratory_work_1/finance/user_repo/auth.py:14:20"
    ```

=== "Обработка токена"

    ```Python
    --8<-- "laboratory_work_1/finance/user_repo/auth.py:20:40"
    ```

=== "Текущий пользователь"

    ```Python
    --8<-- "laboratory_work_1/finance/user_repo/auth.py:40:"
    ```

Эндпойнты для пользователя:

=== "Регистрация"

    ```Python
    from fastapi import APIRouter, HTTPException, Depends
    from user_repo.auth import AuthHandler
    from sqlalchemy.orm import Session
    from connections import get_session
    from user_repo.user_models import UserInput, User, UserLogin, UserPasswordChange
    from user_repo.user_functions import select_all_users, find_user
    
    user_router = APIRouter()
    auth_handler = AuthHandler()

    --8<-- "laboratory_work_1/finance/user_repo/user_endpoints.py:11:24"
    ```

=== "Вход"

    ```Python
    from fastapi import APIRouter, HTTPException, Depends
    from user_repo.auth import AuthHandler
    from sqlalchemy.orm import Session
    from connections import get_session
    from user_repo.user_models import UserInput, User, UserLogin, UserPasswordChange
    from user_repo.user_functions import select_all_users, find_user
    
    user_router = APIRouter()
    auth_handler = AuthHandler()

    --8<-- "laboratory_work_1/finance/user_repo/user_endpoints.py:25:36"
    ```

=== "Текущий юзер и список юзеров"

    ```Python
        from fastapi import APIRouter, HTTPException, Depends
    from user_repo.auth import AuthHandler
    from sqlalchemy.orm import Session
    from connections import get_session
    from user_repo.user_models import UserInput, User, UserLogin, UserPasswordChange
    from user_repo.user_functions import select_all_users, find_user
    
    user_router = APIRouter()
    auth_handler = AuthHandler()

    --8<-- "laboratory_work_1/finance/user_repo/user_endpoints.py:37:51"
    ```
=== "Смена пароля"

    ```Python
    from fastapi import APIRouter, HTTPException, Depends
    from user_repo.auth import AuthHandler
    from sqlalchemy.orm import Session
    from connections import get_session
    from user_repo.user_models import UserInput, User, UserLogin, UserPasswordChange
    from user_repo.user_functions import select_all_users, find_user
    
    user_router = APIRouter()
    auth_handler = AuthHandler()

    --8<-- "laboratory_work_1/finance/user_repo/user_endpoints.py:52:"
    ```

