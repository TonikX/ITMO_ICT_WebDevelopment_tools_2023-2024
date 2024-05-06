# Поиск поездок и попутчиков

## Обзор функционала поиска

Пользователи могут искать поездки и попутчиков с помощью двух основных эндпойнтов: `/trips/` для
общего
поиска поездок и `/trips/my/` для поиска своих поездок. Оба эндпойнта предоставляют возможности
фильтрации, поиска и пагинации.

### 1. Общий поиск поездок

Этот запрос позволяет пользователям находить доступные поездки, используя различные параметры
фильтрации и поиска.

#### Процесс:

1. **Авторизация:** Пользователь должен быть авторизован.
2. **Ввод параметров поиска:** Пользователь может использовать фильтры и параметры поиска для
   уточнения запроса.
3. **Получение данных:** Сервер возвращает список поездок, соответствующих заданным критериям.

#### Реализация:

```python
@router.get('/', response_model=Annotated[list[TripMulti], Depends()])
async def get_trips(
    user: Annotated[User, Depends(get_user)],
    filter_params: Annotated[FilterParams, Depends(get_filter_params)],
    search_param: Annotated[SearchParam, Depends(get_search_param)],
    pag_params: Annotated[PaginationParams, Depends(get_pagination_params)]
):
    return await repository.get_many_trips_filters(
        filter_params=filter_params,
        search_param=search_param,
        pag_params=pag_params
    )
```

### 2. Поиск своих поездок

Этот запрос позволяет пользователю искать поездки, созданные им самим.

#### Процесс:

1. **Авторизация:** Пользователь должен быть авторизован и иметь профиль.
2. **Ввод параметров поиска:** Пользователь может фильтровать и искать свои поездки.
3. **Получение данных:** Сервер возвращает список созданных пользователем поездок, соответствующих
   критериям.

#### Реализация:

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

## Функции поиска и фильтрации

- **Фильтры:** Пользователи могут применять фильтры, такие как дата поездки, место отправления и
  место прибытия.
- **Поиск:** Поиск по ключевым словам в описании поездок.
- **Пагинация:** Поддержка пагинации для удобной навигации по страницам результатов.
