# Механизм авторизации с использованием JWT

## Эндпойнты

### Регистрация пользователя

- **Метод:** `POST`
- **URL:** `/auth/register/`
- **Описание:** Регистрирует нового пользователя в системе.

#### Процесс:

1. **Проверка наличия пользователя:** Сначала проверяется, существует ли уже пользователь с таким же
   email.
2. **Обработка ошибок:** Если пользователь с таким email уже существует, возвращается
   ошибка `400 Bad Request` с сообщением "Email already registered".
3. **Создание пользователя:** Если email свободен, создается новый пользователь с хешированным
   паролем.

#### Реализация:

```python
@router.post('/register/', response_model=Annotated[UserPrivate, Depends()])
async def register(
    credentials: Annotated[UserCredentials, Body()]
):
    is_exists = await repository.exists(email=credentials.email)

    if is_exists:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Email already registered'
        )

    return await repository.create(
        dict(
            email=credentials.email,
            hashed_password=hash_password(credentials.password)
        )
    )
```

### Логин пользователя

- **Метод:** `POST`
- **URL:** `/auth/login/`
- **Описание:** Аутентифицирует пользователя и возвращает JWT.

#### Процесс:

1. **Получение пользователя по email:** Сначала извлекается пользователь по указанному email.
2. **Валидация пароля:** Проверяется, совпадает ли предоставленный пароль с хешированным паролем в
   базе данных.
3. **Обработка ошибок:** Если пользователь не найден или пароль неверный, возвращается
   ошибка `401 Unauthorized` с сообщением "Invalid credentials".
4. **Создание JWT:** При успешной валидации создается и возвращается JWT.

#### Реализация:

```python
@router.post('/login/', response_model=Annotated[JWT, Depends()])
async def login(
    credentials: Annotated[UserCredentials, Body()]
):
    user = await repository.get_one(email=credentials.email)

    if not (
        user and
        validate_password(credentials.password, user.hashed_password)
    ):
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            'Invalid credentials'
        )

    return create_jwt(user)
```