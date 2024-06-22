# Задание №4

Реализуем документацию средствами Swagger. Для начала, заполним конфигурацию.

Т.к. на все запросы стоит миддлвейр на авторизацию, предусмотрим возможность авторизации с помощью указания sign ключа.

### swagger.ts

```typescript
const swaggerJsDoc = require("swagger-jsdoc");

const swaggerOptions = {
  swaggerDefinition: {
    openapi: "3.0.0",
    info: {
      title: "Sheep Royale API",
      version: "1.0.0",
      description: "API игры Sheep Royale",
    },
    servers: [
      {
        url: "http://localhost:30000",
        description: "Local server",
      },
    ],
    components: {
      securitySchemes: {
        signKeyAuth: {
          type: "apiKey",
          in: "header",
          name: "Authorization",
          description:
            "Введите ваш sign ключ из под мини-приложения внутри социальной сети",
        },
      },
    },
    security: [
      {
        signKeyAuth: [],
      },
    ],
  },
  apis: ["./**/*.ts"], // Указываем путь к вашим маршрутам
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);

module.exports = swaggerDocs;
```

Затем, подключим swagger в корне бекенда

### index.ts

```typescript
app.use("/api-docs", swaggerUi.serve, swaggerUi.setup(swaggerDocs));
```

И, наконец, добавим необходимую документацию.

Для user/get ничего кроме авторизации не потребуется, а вот для user/bonuses укажем все доступные варианты параметра methodName при получении бонуса.

### routes/user/index.ts

```typescript
/**
 * @swagger
 * /user/get:
 *   get:
 *     summary: Возвращает информацию о пользователе
 *     tags:
 *       - User
 *     security:
 *       - signKeyAuth: []
 *     responses:
 *       200:
 *         description: Успешный ответ с информацией о пользователе
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 userId:
 *                   type: string
 *                   description: ID пользователя
 *                 platform:
 *                   type: string
 *                   description: Платформа пользователя
 *                 name:
 *                   type: string
 *                   description: Имя пользователя
 *                 photo_200:
 *                   type: string
 *                   description: Фото пользователя
 *                 balance:
 *                   type: integer
 *                   description: Баланс пользователя
 *                 tasks:
 *                   type: object
 *                   description: Задачи пользователя
 *                 units:
 *                   type: array
 *                   items:
 *                     type: object
 *                   description: Коллекция карточек пользователя
 *                 emotions:
 *                   type: array
 *                   items:
 *                     type: object
 *                   description: Эмоции пользователя
 *                 chests:
 *                   type: array
 *                   items:
 *                     type: object
 *                   description: Сундуки пользователя
 *       500:
 *         description: Не удалось получить данные о пользоавтеле от социальной сети
 */
router.get("/get", getUser);

/**
 * @swagger
 * /user/bonuses:
 *   get:
 *     summary: Обработка бонусов пользователя
 *     tags:
 *       - User
 *     security:
 *       - signKeyAuth: []
 *     parameters:
 *       - in: query
 *         name: methodName
 *         required: true
 *         schema:
 *           type: string
 *           enum: [joinChat, subGroup, notificationApp, notificationBot, addToFavorites, daily, rewardedGift, refreshGift, addToHomeScreen]
 *         description: Метод получения бонуса
 *     responses:
 *       200:
 *         description: Успешный ответ с информацией о балансе пользователя и бонусах
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 balance:
 *                   type: integer
 *                   description: Текущий баланс пользователя
 *                 time:
 *                   type: integer
 *                   description: Время до следующего бонуса
 *                 adWatchedTimes:
 *                   type: integer
 *                   description: Количество просмотренных реклам (для rewardedGift)
 *                 bonuses:
 *                   type: string
 *                   description: Название метода получения бонуса
 *       400:
 *         description: Ошибка валидации запроса или отсутствует конфигурация
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 error:
 *                   type: string
 *                   description: Описание ошибки
 *       500:
 *         description: Внутренняя ошибка сервера
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 message:
 *                   type: string
 *                   description: Описание ошибки
 */
router.get("/bonuses", bonuses);
```

Для получения статусов ничего дополнительно не нужно, а для установки заложим vkStatusId, для установки конкретного статуса.

### routes/statuses/index.ts

```typescript
/**
 * @swagger
 * /user/statuses/get:
 *   get:
 *     summary: Возвращает актуальную информацию о статусах пользователя
 *     tags:
 *       - User
 *     security:
 *       - signKeyAuth: []
 *     responses:
 *       200:
 *         description: Успешный ответ с актуальной информацией о статусах пользователя
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   statusId:
 *                     type: string
 *                     description: ID статуса
 *                   name:
 *                     type: string
 *                     description: Название статуса
 *                   isSelected:
 *                     type: boolean
 *                     description: Статус выбран или нет
 *                   isGiftReceived:
 *                     type: boolean
 *                     description: Получен ли подарок за статус
 *       404:
 *         description: Пользователь не найден
 *       500:
 *         description: Внутренняя ошибка сервера
 */
router.get("/get", getStatuses);
/**
 * @swagger
 * /user/statuses/set:
 *   post:
 *     summary: Устанавливает статус пользователя
 *     tags:
 *       - User
 *     security:
 *       - signKeyAuth: []
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               vkStatusID:
 *                 type: integer
 *                 description: ID статуса VK
 *     responses:
 *       200:
 *         description: Успешный ответ с обновленной информацией о статусе пользователя
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 updatedStatus:
 *                   type: object
 *                   description: Обновленный статус пользователя
 *                 collection:
 *                   type: array
 *                   items:
 *                     type: object
 *                   description: Коллекция карточек пользователя
 *                 balance:
 *                   type: integer
 *                   description: Баланс пользователя
 *                 items:
 *                   type: array
 *                   items:
 *                     type: object
 *                   description: Лут, полученный за статус
 *       400:
 *         description: Ошибка валидации запроса
 *       500:
 *         description: Внутренняя ошибка сервера или статус отсутствует в БД
 */
router.post("/set", setStatus);
```
