# Роуты

## Users

- /users/ Post - регистрация ready

- /users/login Post - получение JWT токена ready

- /users/getSelf Get - получение информации о себе ready

- /users/resetPassword Post - сброс пароля

## Books

- /books/ Get - поиск по всем книгам в библиотеки ready

- /books/ Post - создане запроса на добавление книги ready

- /books/id Get - Просмотр конкретной книги ready

- /books/id Put - Изменение статуса книги. Только для админов ready

- /books/owned Post - добавление владениея книгой ready

## Wishlists

- /wishlists/id Get - Просмотр вишлиста пользователя ready

- /wishlists/id Post - Добавить книгу в лист ready

- /wishlists/id Delete - Удалить книгу из листа ready

## ExchangeRequests

- /exchangeRequests Get - Просмотр ваших реквестов на обмен

- /exchangeRequests Post - Создание запроса на обмен

- /exchangeRequests Put - Изменить статус запроса. Можно подтвердить
