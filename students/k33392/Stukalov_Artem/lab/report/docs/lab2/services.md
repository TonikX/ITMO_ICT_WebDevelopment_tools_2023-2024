# Сервисы

Набор функций для взаимодействия с каждоый моделью. Предполагается, сервис не должен быть завязан на используемые роуты.

- `auth` - сревис аутентификации пользователя при помощи JWT токенов.
- `books` - сервис отвечающий за рпботу с моделями `books`
- `exchange_requests` - сервис отвечающий за рпботу с моделями `exchange_requests`
- `users` - сервис отвечающий за рпботу с моделями `users`
- `wishlists` - сервис отвечающий за рпботу с моделями `wishlists`

=== "auth"

    ```Python title="Auth"
    --8<-- "lab-2/src/services/auth.py"
    ```

=== "books"

    ```Python title="Books"
    --8<-- "lab-2/src/services/books.py"
    ```

=== "ExchangeRequests"

    ```Python title="ExchangeRequests"
    --8<-- "lab-2/src/services/exchange_requests.py"
    ```

=== "users"

    ```Python title="Users"
    --8<-- "lab-2/src/services/users.py"
    ```

=== "wishlists"

    ```Python title="Wishlists"
    --8<-- "lab-2/src/services/wishlists.py"
    ```
