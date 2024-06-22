# Задание №3

Реализуем базовые утилиты и роуты.

## Сервер (src/models/Users/utils/getUserModel.ts):

Т.к. в первом задании мы раздили пользователей на три коллекции, реализуем функцию которая будет возвращать необходимую коллекцию в зависимости от платформы пользователя

```typescript
import { Platforms } from "@/src/types/platforms";
import { Users } from "../Users";
import { UsersOk } from "../UsersOk";
import { UsersTg } from "../UsersTg";

function UsersModel(platform: Platforms) {
  switch (platform) {
    case Platforms.vk:
      return Users;
    case Platforms.tg:
      return UsersTg;
    case Platforms.ok:
      return UsersOk;
  }
}
export default UsersModel;
```

## Сервер (hub/utils/findUser.ts):

Теперь сделаем функцию которая будет возвращать пользователя по его id. А если пользователя ещё нет - будет его создавать. Учтем в ней необходимость использовать её с учетом разниы в платформах (ОК, ТГ, ВК)

```typescript
import "../models/Lobbies";
import { recordUserAction } from "@/instances/hub/src/utils/recordUserAction";
import { IGetUserIDAuthInfo } from "@/instances/hub/src/types/request";
import { userInfoPlatform } from "./userInfo";
import { IUserWithEmotions, Users } from "../models/Users/Users";
import { Platforms } from "../types/platforms";
import UsersModel from "../models/Users/utils/getUsersModel";
import { newUserMessage } from "@/instances/hub/src/utils/tasks/checkTasks";
import { ONLINE_SECONDS_TIMEOUT } from "../configs/online";

// Базовые параметры которые всегда будут находиться в req, на случай если пользователя нужно будет создать
export type findUserParams = IGetUserIDAuthInfo & {
  userRegistrationData?: {
    firstName: string;
    lastName?: string;
  };
};

export const findUser = async (req: findUserParams) => {
  try {
    let user;
    req.userId = Number(req.userId);

    // Пытаемся найти пользователя в базе
    user = await UsersModel(req.platform)
      .findOne({ _id: req.userId })
      .populate("lobby")
      .populate<Pick<IUserWithEmotions, "emotions">>("emotions.emotion");

    // Создаем пользователя, если его ещё нет
    if (!user) {
      let usersInfo;

      // Получаем данные пользователя, такие как имя, аватар и др.
      usersInfo = await userInfoPlatform({
        userId: req.userId,
        platform: req.platform,
        authorization: req.hash,
        userRegistrationData: req.userRegistrationData,
      });

      if (!usersInfo) {
        throw new Error("failed to get user info for create");
      }

      const userInfo = usersInfo[0];

      const date = new Date();

      let userData = {
        _id: req.userId,
        platform: userInfo.platform,
        name: userInfo.name,
        photo_100: userInfo.photo_100,
        photo_200: userInfo.photo,
        registrationDate: date.toISOString(),
        referrals: {},
        bonuses: { notificationBot: false },
      };

      // Отмечаем для телеграмма, если пользователь разрешил ему написать от лица бота
      if (userInfo.platform === Platforms.tg && req?.allowsWriteToPmTg) {
        userData.bonuses.notificationBot = true;
      }

      // Определеяем пришел ли пользователь как реферал
      const referrerID = Number(req?.userRefferal);

      // Если передан ref, проверяем валидность всех данных и обновляем модели сохраняя реферала
      if (referrerID) {
        console.info("ref", referrerID, req.platform);
        const referrer = await UsersModel(req.platform).findOne({
          _id: referrerID,
        });
        /**
         * В каких случаях отдаем ошибку:
         * 1. Если referrer не найден (тот, кто пригласил в игру)
         * 2. Если айди приглашающего совпадает с приглашенным (пригласил сам себя)
         */

        if (!referrer || req.userId === referrerID) {
        } else {
          // Сохраняем айди, чтобы чуть позже выдать бонус
          userData = { ...userData, referrals: { refId: String(referrerID) } };
        }
      }
      let user;

      // Создаем пользователя в нужной модели
      user = await UsersModel(req.platform).create(userData);

      if (!user) throw new Error("failed to create user");

      // Используя реф получаем данные о доступных пользователю эмоциях
      user = await user.populate<Pick<IUserWithEmotions, "emotions">>(
        "emotions.emotion"
      );

      // Записываем события пользователей ВК в аналитику
      req.platform === Platforms.vk &&
        recordUserAction(user._id, "registration", {
          vkRef: req?.userRef,
          vkPlatform: req?.userVkPlatform,
          vkInitialParams: req?.authorization,
          hash: req?.hash,
        });

      return user;
    }

    // Кешируем счетчик онлайна
    redis.setex(
      `online_list:${user._id}`,
      ONLINE_SECONDS_TIMEOUT,
      user._id + ""
    );

    return user;
  } catch (e) {
    console.log("Find User Error", e);
  }
};
```

## Сервер (hub/routes/user/getUser.ts):

Реализуем эндпоинт возвращающий пользовательские данные.

```typescript
import { ICard, IChestDocs } from "@/src/models/Users/Users";
import { findShop } from "@/src/utils/findShop";
import { MIN_RATING } from "@src/data/rating";
import { findUser } from "@src/utils/findUser";
import { Response } from "express";
import { IGetUserIDAuthInfoRequest } from "../../types/request";
import { getCollection } from "../../utils/getCardsInfo";
import { shopContentUpdate } from "../shop/getContent";
import { getUserEmotions } from "../../utils/emotions/getUserEmotions";
import { recordUserAction } from "../../utils/recordUserAction";
import { refreshRewardedGiftTime } from "../../utils/refreshRewardedGiftTime";
import { GAME_HISTORY_LENGTH } from "@/src/configs/users";

import { userInfoPlatform } from "@/src/utils/userInfo";
import { newUserMessage } from "../../utils/tasks/checkTasks";
import { Platforms } from "@/src/types/platforms";

export default async function (req: IGetUserIDAuthInfoRequest, res: Response) {
  const user = await findUser(req);

  if (!user) return;

  const userPlatform = user.platform;

  let saveFlag = false;

  // Запрашиваем новый аватар и имя пользователя, на случай если он изменился
  const usersInfo = await userInfoPlatform({
    userId: user._id,
    platform: user.platform,
    authorization: req.authorization,
  });

  if (!usersInfo?.length) {
    res.status(500).json({
      message: "failed to get user info",
    });
    return;
  }

  const userInfo = usersInfo[0];

  // Сохраняем обновленные данные если изменение произошло
  if (user.photo_200 != userInfo.photo || user.name != userInfo.name) {
    user.photo_200 = userInfo.photo;
    user.name = userInfo.name;

    saveFlag = true;
  }

  if (saveFlag) {
    await user.save();
  }

  // Отправляем пользователю список ежедневных заданий, если сегодня он ещё не получал их через чат-бота
  if (user.bonuses.notificationBot && user.tasks.nextUpdateAt <= Date.now()) {
    const oldUpdateTime = user.tasks.nextUpdateAt;
    newUserMessage(user._id, oldUpdateTime, userPlatform);
  }
  await refreshRewardedGiftTime(user);

  const { cards, ...userObject } = user.toObject();

  // Собираем данные для отправки на клиент
  const response = {
    ...userObject,
    units: getCollection(cards),
    emotions: await getUserEmotions(user),
    chests: (user.chests as IChestDocs).map((doc) => {
      const { _id, willOpenAt, ...chest } = doc.toObject() as any;
      return chest.empty
        ? null
        : {
            ...chest,
            willOpenAt:
              willOpenAt === undefined ? undefined : willOpenAt - Date.now(),
          };
    }),
  };

  // Собираем аналитику по пользователям
  recordUserAction(userObject._id, "login");

  res.status(200).json(response);
}
```

## Сервер (hub/routes/user/completeBonuses.ts):

Реализуем роут который будет обрабатывать выполнение бонусных заданий пользователем. Таких как подписаться на группу ВК, вступить в чат и тд.

```typescript
import { IGetUserIDAuthInfoRequest } from "../../types/request";
import { findUser } from "@src/utils/findUser";
import { Response } from "express";
import { group } from "@/src/utils/vkapi";
import { format } from "util";

import { recordUserAction } from "../../utils/recordUserAction";
import { Configs } from "@/src/models/Configs";
import { refreshRewardedGiftTime } from "../../utils/refreshRewardedGiftTime";
import { convertTasksToText } from "@/instances/bot/src/service/tasks/convertTasksToText";
import { generateTasks } from "@/instances/bot/src/service/tasks/generateTasks";
import { WELCOME_AFTER_BONUS } from "@/instances/bot/config/text";
import { TasksListKeyboard } from "@/instances/bot/config/keyboard/Keyboard";

type ALLOWED_VK_METHODS =
  | "joinChat"
  | "subGroup"
  | "notificationApp"
  | "notificationBot"
  | "addToFavorites"
  | "daily"
  | "rewardedGift"
  | "refreshGift"
  | "addToHomeScreen";

// Определяем стоимость каждого из заданий
const VKMETHODS_COST = {
  joinChat: 50,
  subGroup: 50,
  notificationApp: 50,
  notificationBot: 100,
  addToFavorites: 50,
  daily: 50,
  rewardedGift: 50,
  refreshGift: 50,
  addToHomeScreen: 100,
};

export default async function (req: IGetUserIDAuthInfoRequest, res: Response) {
  const user = await findUser({
    userId: req.userId,
    platform: req.platform,
  });
  const oneDay = 24 * 60 * 60 * 1000;
  const method = req.query.methodName as ALLOWED_VK_METHODS;

  if (!user) return res.status(400).json({ error: "no_user" });

  if (!ArrayVKMETHODS.includes(method)) return; // Игнорируем методы вне списка разрешенных методов

  // Обрабатываем логику ежедневного бонуса
  if (method === "daily") {
    if (user.bonuses.daily <= Date.now()) {
      user.balance += 100;
      user.bonuses.daily = Date.now() + oneDay;
      res.status(200).json({
        balance: user.balance,
        time: user.bonuses.daily,
      });

      await user.save();
    }
  } else if (method === "refreshGift") {
    // Обрабатываем логику подарка который можно забирать 1 раз в сутки

    await refreshRewardedGiftTime(user);

    res.status(200).json({
      balance: user.balance,
      time: user.bonuses.rewardedGift.lastUpdate,
      adWatchedTimes: user.bonuses.rewardedGift.adWatchedTimes,
    });
  } else if (method === "rewardedGift") {
    // Обрабатываем логику подарка который можно забирать по 5 раз каждые сутки за просмотр рекламы
    const rewardedGiftDocument = await Configs.findOne({
      name: "REWARDED_GIFT",
    });

    if (!rewardedGiftDocument)
      return res.status(400).json({ error: "no_config" });
    if (!rewardedGiftDocument.values)
      return res.status(400).json({ error: "no_value_in_config" });

    const maxAdWatchedTimes = rewardedGiftDocument.values.maxAdWatchedTimes;
    const value = rewardedGiftDocument.values.value;

    if (!maxAdWatchedTimes)
      return res.status(400).json({ error: "no_value_in_config" });
    if (!value) return res.status(400).json({ error: "no_value_in_config" });
    if (user.bonuses.rewardedGift.adWatchedTimes <= maxAdWatchedTimes) {
      user.bonuses.rewardedGift.adWatchedTimes += 1;

      user.balance += value;

      res.status(200).json({
        balance: user.balance,
        time: user.bonuses.rewardedGift.lastUpdate,
        adWatchedTimes: user.bonuses.rewardedGift.adWatchedTimes,
      });
      await user.save();
    }
  } else {
    // Для остальных бонусов проверяем что они ещё не были получены
    if (user.bonuses[method] !== true) {
      // Если это задание на включение уведомлений от чат-бота, формируем и отправляем пользователю заданий на день
      if (
        method === "notificationBot" &&
        user.tasks.nextUpdateAt <= Date.now()
      ) {
        try {
          const tasks = await generateTasks(user.cards);
          user.tasks = tasks;
          // [ANALYTICS]
          recordUserAction(user._id, "dailyTasksReceived", {
            tasks: user.tasks.current,
          });
          user.markModified("tasks");

          group.api.messages
            .send({
              user_id: user._id,
              message: format(
                WELCOME_AFTER_BONUS,
                await convertTasksToText(user.tasks)
              ),
              keyboard: TasksListKeyboard(),
              random_id: Date.now(),
            })
            .catch(() => null);
        } catch {}
      }
      // В остальных случаях засчитываем выполнение и обновляем баланс
      user.bonuses[method] = true;
      user.balance += VKMETHODS_COST[method];
      res.status(200).json({ balance: user.balance, bonuses: method });
      await user.save();
    }
  }
}
```

## Сервер (hub/routes/user/statuses/setStatus.ts):

Реализуем функционал для установки эмодзи-статусы ВКонтакте и отображения его в интерфейсе.

```typescript
import { Response } from "express";
import { EmojiStatuses, PopulatedIStatus } from "@src/models/Statuses";
import { ChestsData } from "@src/data/chests";
import { lootGenerate } from "@hub/src/utils/chestLootGenerate";
import { IGetUserIDAuthInfoRequest } from "@hub/src/types/request";
import { getCollection } from "@hub/src/utils/getCardsInfo";
import { Users } from "@/src/models/Users/Users";
import { checkIsItemUnlocked } from "@/instances/hub/src/utils/quests/checkIsItemUnlocked";
import axios from "axios";

/** Контроллер для установки статуса */

export default async function (req: IGetUserIDAuthInfoRequest, res: Response) {
  const { vkStatusID } = req.body;

  if (!vkStatusID || Number.isNaN(vkStatusID) || !Number.isFinite(vkStatusID)) {
    return res.status(400).json();
  }

  const user = await Users.findById(req.userId).populate("statuses");
  if (!user) return;

  if (!user) {
    return res.status(500).json();
  }

  try {
    const updatedStatus = await EmojiStatuses.findOne({
      vkStatusID,
    }).populate<PopulatedIStatus>("requiredQuest");

    if (!updatedStatus) {
      return res.status(500).json("Can't set this status");
    }

    const userStatus = user.statuses.find((userStatus) => {
      return userStatus.status.toString() === updatedStatus._id.toString();
    });

    /** Нельзя установить статус, которого нет в массиве у юзера**/
    if (!userStatus) {
      return res.status(500).json("No status in the user model");
    }

    const isSelectedExist = user.statuses.find(
      (userStatus) => userStatus.isSelected
    );

    if (isSelectedExist) {
      isSelectedExist.isSelected = false;
    }

    // Отправляем запрос в ВК на установку статуса
    const response = await axios.get<any>(
      "https://api.vk.com/method/status.setImage",
      {
        params: {
          status_id: vkStatusID,
          access_token: process.env.APP_TOKEN,
          user_id: user._id,
          v: "5.100",
        },
      }
    );

    // Отмечаем статус как выбранный
    userStatus.isSelected = true;

    if (userStatus.isGiftReceived) {
      await user.save();
      return res.status(200).json({ updatedStatus });
    }
    // Генерируем лут на случай если сундук за статус ещё не был получен
    const chestType = updatedStatus.giftChestType;
    const loot = ChestsData[chestType].loot;
    const items = lootGenerate(loot, user);

    userStatus.isGiftReceived = true;

    await user.save();

    const { collection } = getCollection(user.cards);

    return res.status(200).json({
      updatedStatus,
      collection,
      balance: user.balance,
      items,
    });
  } catch (error) {
    return res.status(500).json(error);
  }
}
```

## Сервер (hub/routes/user/statuses/getStatus.ts):

Реализуем функционал для получения текущего установленного эмодзи-статуса пользователя ВКонтакте.

```typescript
import { findUser } from "@src/utils/findUser";
import { IGetUserIDAuthInfoRequest } from "@hub/src/types/request";
import { Response } from "express";
import { userStatusesUpdate } from "../../../utils/statuses/getUserStatuses";

/** Возвращает актуальную информацию о статусах пользователя */
export default async function (req: IGetUserIDAuthInfoRequest, res: Response) {
  try {
    const user = await findUser({
      userId: req.userId,
      platform: req.platform,
    });
    if (!user) {
      return res.status(404).json();
    }
    // Вызываем функцию обновления статусов
    const statuses = await userStatusesUpdate(user);

    // Возвращаем ответ на клиент
    return res.status(200).json(statuses);
  } catch (error) {
    console.error("Error: ", error);
    return res.status(500).json();
  }
}
```

## Сервер (hub/routes/user/utils/userStatusesUpdate.ts):

```typescript
import { EmojiStatuses, PopulatedIStatus } from "@src/models/Statuses";
import { Document } from "mongoose";
import { IUser, UserStatus } from "@/src/models/Users/Users";
import { checkIsItemUnlocked } from "@/instances/hub/src/utils/quests/checkIsItemUnlocked";

/** Актуализирует информацию о доступных статусах для юзера */
export async function userStatusesUpdate(
  user: Document<unknown, any, IUser> &
    Omit<IUser & Required<{ _id: number }>, never>
): Promise<UserStatus[]> {
  try {
    // Отправляет запрос в базу данных для получения статусов и заданий необходимых для их разблокировки
    const statuses = await EmojiStatuses.find().populate<PopulatedIStatus>(
      "requiredQuest"
    );

    for (const status of statuses) {
      /** Если статус не доступен юзеру или он уже есть у юзера в моделе, то идем дальше */
      if (
        user.statuses.find(
          (userStatus) =>
            userStatus.status._id.toString() === status._id.toString()
        ) ||
        (status?.requiredQuest &&
          !checkIsItemUnlocked(status.requiredQuest.requirements, user))
      ) {
        continue;
      }

      const statusId = status._id;

      const userStatus = user.statuses.find(
        (userStatus) => userStatus.status === statusId
      );

      /** Если статус доступен и он уже в массиве, то идем дальше */
      if (userStatus) {
        continue;
      }
      // Если задание выполнено, добавляем пользователю статус в его массив
      user.statuses.push({
        status: statusId,
        isSelected: false,
        isGiftReceived: false,
      });
    }

    await user.save();

    return user.statuses;
  } catch (error) {
    throw error;
  }
}
```