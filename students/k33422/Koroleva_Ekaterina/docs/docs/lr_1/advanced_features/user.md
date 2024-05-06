# Управление профилем пользователя

## Эндпойнты

### Изменение пароля

- **Метод:** `POST`
- **URL:** `/users/change-password/`
- **Описание:** Позволяет пользователю изменить свой пароль.

#### Реализация:

```python
@router.post('/change-password/', response_model=Annotated[Message, Depends()])
async def change_password(
    data: Annotated[PasswordChange, Body()],
    user: Annotated[User, Depends(get_user)]
):
    if not validate_password(
        data.old_password,
        user.hashed_password
    ):
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            'Invalid old password'
        )

    await repository.update(
        dict(
            hashed_password=hash_password(data.new_password)
        ),
        id=user.id
    )

    return Message(msg='Success')
```

#### Детали реализации:

1. **Валидация старого пароля:** Сначала проверяется правильность введенного старого пароля.
2. **Обработка ошибок:** Если старый пароль неверен, возвращается ошибка `400 Bad Request` с
   сообщением "Invalid old password".
3. **Обновление пароля:** При успешной валидации старого пароля происходит хеширование нового пароля
   и его сохранение в базе данных.
4. **Ответ:** Возвращается сообщение об успешном изменении пароля.

### Получение информации о профиле

- **Метод:** `GET`
- **URL:** `/users/me/`
- **Описание:** Возвращает данные профиля текущего пользователя.

#### Реализация:

```python
@router.get('/me/', response_model=Annotated[UserMe, Depends()])
async def get_me(
    user: Annotated[User, Depends(get_user_profile)]
):
    return user
```

#### Детали реализации:

- **Ответ:** Возвращается полная информация о профиле пользователя, включая личные данные и
  настройки.

### Обновление профиля

- **Метод:** `PUT`
- **URL:** `/users/me/`
- **Описание:** Позволяет полностью обновить данные профиля пользователя.

#### Реализация:

```python
@router.put('/me/', response_model=Annotated[UserMe, Depends()])
async def update_me(
    data: Annotated[ProfileUpdate, Body()],
    user: Annotated[User, Depends(get_user_profile)]
):
    profile = await repository.update(data.model_dump(), user_id=user.id)

    return concat_user_profile(user, profile)

```

#### Детали реализации:

- **Обновление данных:** Производится обновление всех данных профиля на основе предоставленной
  информации.
- **Ответ:** Возвращается обновленная информация о профиле пользователя.

### Частичное обновление профиля

- **Метод:** `PATCH`
- **URL:** `/users/me/`
- **Описание:** Позволяет частично обновить данные профиля пользователя.

#### Реализация:

```python
@router.patch('/me/', response_model=Annotated[UserMe, Depends()])
async def partial_update_me(
    data: Annotated[ProfilePartialUpdate, Body()],
    user: Annotated[User, Depends(get_user_profile)]
):
    profile = await repository.update(
        data.model_dump(exclude_none=True),
        user_id=user.id
    )

    return concat_user_profile(user, profile)
```

#### Детали реализации:

- **Частичное обновление:** Обновляются только те поля профиля, которые были предоставлены в
  запросе.
- **Ответ:** Возвращается обновленная информация о профиле пользователя.

### Удаление профиля

- **Метод:** `DELETE`
- **URL:** `/users/me/`
- **Описание:** Удаляет профиль пользователя из системы.

#### Реализация:

```python
@router.delete('/me/', response_model=Annotated[Message, Depends()])
async def delete_me(
    user: Annotated[User, Depends(get_user_profile)]
):
    await repository.delete(user_id=user.id)
    return Message(msg='Success')
```

#### Детали реализации:

- **Удаление профиля:** Полное удаление всех данных пользователя из базы данных.
- **Ответ:** Возвращается сообщение об успешном удалении профиля.
