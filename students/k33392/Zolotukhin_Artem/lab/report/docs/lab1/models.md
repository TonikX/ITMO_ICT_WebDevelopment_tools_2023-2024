# Модели БД

Главным образом есть 5 моделей:

- `User` - Пользователь сервиса
- `Book` - Книга, информация о которой есть в сервисе
- `ExchangeRequest` - Запрос на обмен экземпляром книги
- `BookOwnership` - Информация о владении экземпляром книги
- `WishlistItem` - Книга в вишлисте пользователя

=== "User"

    ```Python title="User"
    --8<-- "lab-1/src/models.py:111:131"
    ```

=== "Book"

    ```Python title="Book"
    --8<-- "lab-1/src/models.py:140:154"
    ```

=== "ExchangeRequest"

    ```Python title="ExchangeRequest"
    --8<-- "lab-1/src/models.py:52:75"
    ```

=== "BookOwnership"

    ```Python title="BookOwnership"
    --8<-- "lab-1/src/models.py:9:12"
    ```

=== "WishlistItem"

    ```Python title="WishlistItem"
    --8<-- "lab-1/src/models.py:15:18"
    ```
