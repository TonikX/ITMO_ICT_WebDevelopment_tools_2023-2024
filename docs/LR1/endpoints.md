# Эндпоинты

Модуль описывает основные эндпоинты для управления категориями, периодами, затратами и доходами.

## Роуты

### Категории

#### POST /category-create
Создает новую категорию.

#### GET /list-categories
Возвращает список всех категорий.

#### GET /category/{category_id}
Возвращает информацию о категории по `category_id`.

#### PATCH /category/update/{category_id}
Обновляет информацию о категории по `category_id`.

#### DELETE /category/delete/{category_id}
Удаляет категорию по `category_id`.

### Периоды

#### POST /period-create
Создает новый период.

#### GET /list-periods
Возвращает список всех периодов.

#### GET /period/{period_id}
Возвращает информацию о периоде по `period_id`.

#### PATCH /period/update/{period_id}
Обновляет информацию о периоде по `period_id`.

#### DELETE /period/delete/{period_id}
Удаляет период по `period_id`.

### Затраты

#### POST /waste-create
Создает новую запись о затратах.

#### GET /list-wastes
Возвращает список всех затрат.

#### GET /waste/{waste_id}
Возвращает информацию о затрате по `waste_id`.

#### PATCH /waste/update/{waste_id}
Обновляет информацию о затрате по `waste_id`.

#### DELETE /waste/delete/{waste_id}
Удаляет запись о затрате по `waste_id`.

### Доходы

#### POST /income-create
Создает новую запись о доходе.

#### GET /list-incomes
Возвращает список всех доходов.

#### GET /income/{income_id}
Возвращает информацию о доходе по `income_id`.

#### PATCH /income/update/{income_id}
Обновляет информацию о доходе по `income_id`.

#### DELETE /income/delete/{income_id}
Удаляет запись о доходе по `income_id`.