# Создание и управление профилями

## Регистрация нового пользователя

При регистрации нового пользователя используется POST запрос на `/auth/register/`. Эндпойнт
принимает
учетные данные пользователя и выполняет следующие шаги:

1. **Проверка наличия пользователя:** Проверяется, зарегистрирован ли уже введенный электронный
   адрес.
2. **Обработка ошибок:** Если пользователь с таким адресом уже существует, возвращается
   ошибка `400 Bad Request` с сообщением "Email already registered".
3. **Создание пользователя:** Если адрес свободен, создается новый пользователь с хешированным
   паролем и указанным электронным адресом.

### Реализация:

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

## Создание профиля пользователя

После регистрации пользователя можно создать профиль через POST запрос на `/users/me/`. Этот запрос
обрабатывает данные профиля и связывает их с пользователем:

1. **Проверка существования профиля:** Проверяется, не создан ли уже профиль для этого пользователя.
2. **Обработка ошибок:** Если профиль уже создан, возвращается ошибка `400 Bad Request` с
   сообщением "Profile already created".
3. **Создание профиля:** Если профиль еще не создан, он формируется из предоставленных данных и
   привязывается к пользователю.

### Реализация:

```python
@router.post('/me/', response_model=Annotated[UserMe, Depends()])
async def create_me(
    data: Annotated[ProfileCreate, Body()],
    user: Annotated[User, Depends(get_user)]
):
    if user.profile is not None:
        raise HTTPException(
            http_status.HTTP_400_BAD_REQUEST,
            'Profile already created'
        )

    profile = await repository.create(
        dict(
            **data.model_dump(),
            user_id=user.id
        )
    )

    return concat_user_profile(user, profile)
```
