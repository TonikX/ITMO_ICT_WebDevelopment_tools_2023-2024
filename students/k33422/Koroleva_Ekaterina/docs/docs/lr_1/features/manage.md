# Управление своими поездками

## Эндпойнты

### 1. Создание поездки

- **Метод:** `POST`
- **URL:** `/trips/my/`
- **Описание:** Позволяет пользователю создать новую поездку, указывая все необходимые детали.
- **Тело запроса:** `CreateMyTrip`
- **Реализация:**

```python
@router.post('/my/', response_model=Annotated[MyTripSingleAfterOperation, Depends()])
async def create_my_trip(
    data: Annotated[CreateMyTrip, Body()],
    user: Annotated[User, Depends(get_user_profile)]
):
    return await repository.create(
        dict(
            **data.model_dump(),
            profile_id=user.profile.id
        )
    )
```

### 2. Получение списка своих поездок

- **Метод:** `GET`
- **URL:** `/trips/my/`
- **Описание:** Возвращает список всех поездок пользователя.
- **Параметры:** Фильтрация, поиск и пагинация.
- **Реализация:**

```python
@router.get('/my/', response_model=Annotated[list[MyTripMulti], Depends()])
async def get_my_trips(
    user: Annotated[User, Depends(get_user_profile)],
    filter_params: Annotated[FilterParams, Depends(get_filter_params)],
    search_param: Annotated[SearchParam, Depends(get_search_param)],
    pag_params: Annotated[PaginationParams, Depends(get_pagination_params)]
):
    return await repository.get_many_trips_filters(
        filter_params=filter_params,
        search_param=search_param,
        pag_params=pag_params,
        profile_id=user.profile.id
    )
```

### 3. Получение деталей конкретной поездки

- **Метод:** `GET`
- **URL:** `/trips/my/{pk}/`
- **Описание:** Позволяет получить подробные сведения о конкретной поездке.
- **Реализация:**

```python
@router.get('/my/{pk}/', response_model=Annotated[MyTripSingle, Depends()])
async def get_my_trip(
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    return trip
```

### 4. Обновление поездки

- **Методы:** `PUT` и `PATCH`
- **URL:** `/trips/my/{pk}/`
- **Описание:** `PUT` используется для полного обновления поездки, `PATCH` для частичного.
- **Реализация (`PUT`):**

```python
@router.put('/my/{pk}/', response_model=Annotated[MyTripSingleAfterOperation, Depends()])
async def update_my_trip(
    data: Annotated[UpdateMyTrip, Body()],
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    result = await repository.update(
        data.model_dump(),
        id=pk,
        profile_id=user.profile.id
    )

    return result
```

- **Реализация (`PATCH`):**

```python
@router.patch('/my/{pk}/', response_model=Annotated[MyTripSingleAfterOperation, Depends()])
async def partial_update_my_trip(
    data: Annotated[PartialUpdateMyTrip, Body()],
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    result = await repository.update(
        data.model_dump(exclude_none=True),
        id=pk,
        profile_id=user.profile.id
    )

    return result
```

### 5. Удаление поездки

- **Метод:** `DELETE`
- **URL:** `/trips/my/{pk}/`
- **Описание:** Удаляет указанную поездку.
- **Реализация:**

```python
@router.delete('/my/{pk}/', response_model=Annotated[Message, Depends()])
async def delete_my_trip(
    user: Annotated[User, Depends(get_user_profile)],
    pk: Annotated[int, Path()]
):
    trip = await repository.get_one_trip(id=pk, profile_id=user.profile.id)

    if trip is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            'Trip not found'
        )

    await repository.delete(id=pk, profile_id=user.profile.id)

    return Message(msg='Success')
```
