# Задание №2

Реализуем авторизацию. Необходимо учесть, что авторизация будет производиться сразу с трех платформ (ВК, ОК, ТГ) и на всех платформах методы для авторизации немного отличаются.

Для начала реализуем middleware который будет обрабатывать все поступающие запросы и вызывать функцию для авторизации пользователя.

## Сервер (hub/middlewares/checkSign.ts):

```typescript
import { Response, NextFunction } from "express";
import { IGetUserIDAuthInfoRequest } from "../types/request";
import { checkSignRestApi as checkSignMiddlewareUtils } from "@src/utils/checkSignRestApi";
import { initData, validate } from "@twa.js/init-data-node";
import { TG_BOT_TOKEN } from "@/src/libs/tg";
import { enviroment } from "@/instances/bot/config/enviroment";
import { Platforms } from "@/src/types/platforms";

export const checkSignMiddleware = (
  req: IGetUserIDAuthInfoRequest,
  res: Response,
  next: NextFunction
) => {
  try {
    if (!req.headers.authorization)
      return res
        .status(400)
        .json({ error: "Authorization header is undefined" });

    // Определяем платформу пользователя
    const platform = req.headers.authorization.includes("vk_user_id")
      ? Platforms.vk
      : req.headers.authorization.includes("is_premium") ||
        req.headers.authorization.includes("auth_date")
      ? Platforms.tg
      : Platforms.ok;

    req.platform = platform;

    // Вызываем проверку токена пользователя
    if (
      !checkSignMiddlewareUtils(
        decodeURIComponent(req.headers.authorization),
        [process.env.VK_SECRET_KEY || "", process.env.VK_SECRET_GAME_KEY || ""],
        platform
      )
    ) {
      // Останавливаем выполнение и возвращаем ошибку, если токен пользователя не прошел проверку
      return res.status(400).json({ error: "Sign is not valid" });
    }

    // В случае авторизации сохраняем необходимые данные, такие как userId, реферал и прочее
    if (platform === Platforms.ok) {
      req.userId = Number(
        req.headers.authorization?.split("logged_user_id=")[1]?.split("&")[0]
      );
      req.userRefferal = decodeURIComponent(req.headers.authorization)
        ?.split("ref=")[1]
        ?.split("&")[0];
    }

    if (platform === Platforms.vk) {
      req.userId = Number(
        req.headers.authorization?.split("vk_user_id=")[1]?.split("&")[0] ||
          req.headers.authorization?.split("viewer_id=")[1]?.split("&")[0]
      );
      req.userRef = req.headers.authorization
        ?.split("vk_ref=")[1]
        ?.split("&")[0];

      req.userRefferal = String(req?.query?.hash)
        ?.split("ref=")[1]
        ?.split("&")[0];
    }

    if (platform === Platforms.tg) {
      const data = tgAuth(req.headers.authorization);

      if (!data?.user) return console.error("TG auth data is not defined");
      req.userId = data.user.id;
      req.userRefferal = req.headers.authorization
        ?.split("ref_")[1]
        ?.split("&")[0];
      // TO DO переделать хранение переменных в req
      req.allowsWriteToPmTg = Boolean(
        req.headers.authorization
          ?.split("allows_write_to_pm%22%3A")[1]
          ?.split("%7D&")[0]
      );
    }

    req.userVkPlatform = req.headers.authorization
      ?.split("vk_platform=")[1]
      ?.split("&")[0];

    req.chatId = decodeURIComponent(req.headers.authorization)
      ?.split("vk_chat_id=")[1]
      ?.split("&")[0];

    req.hash = String(req?.query?.hash);

    req.authorization = req.headers.authorization;

    next();
  } catch (err) {
    console.error(err);
    return res.status(400).json({ error: err });
  }
};

const tgAuth = (sign: string) => {
  try {
    if (enviroment.IS_PRODUCTION) {
      validate(sign, TG_BOT_TOKEN);
    }
  } catch (e) {
    throw new Error("Invalid TG signature");
  }

  const parsedInitData = initData.parse(sign);

  if (!parsedInitData.user) {
    throw new Error("User not found");
  }

  if (parsedInitData.user.isBot) {
    throw new Error("Bots is not allowed");
  }

  return parsedInitData;
};
```

## Сервер (src/utils/checkSignRestApi.ts):

Во всех трех случаях (ВК, ОК, ТГ) социальные сети уже предусмотрели процесс авторизации и его необходимо лишь интегрировать в проект.

1. ВК - при запуске мини-приложения передается строка авторизации содержащая id пользователя, важную информацию и sign ключ. Передаем эту строку на сервер, разбиваем на отдельные значения, шифруем через sha256 с применением секретного ключа, который выдается только разработчику. Если полученная подпись и подпись предоставленная платформой совпали, значит пользователь не подделал свои параметры запуска и мы можем ему доверить.
2. ОК - ситуация аналогичная ВК, отличие лишь в том, что для верификации используются не все, а три параметра и для шифрования выбран md5.
3. ТГ - ситуация аналогичная с ВК, но, не предоставлены детали по алгоритму шифрования. Зато реализована библиотека для валидации параметров, что, в любом случае упрощает работу и сокращет код.

```typescript
import * as crypto from "crypto";
import { initData, validate } from "@twa.js/init-data-node";
import { OK_APPLICATION_SECRET_KEY } from "../libs/ok";
import { TG_BOT_TOKEN } from "../libs/tg";
import { enviroment } from "@/instances/bot/config/enviroment";
import { Platforms } from "../types/platforms";
interface QueryParam {
  key: string;
  value: string;
}

/**
 * Верифицирует параметры запуска.
 * @param searchOrParsedUrlQuery
 * @param {string[]} secretKeys
 * @returns {boolean}
 */
export function checkSignRestApi(
  searchOrParsedUrlQuery: string | URLSearchParams,
  secretKeys: string[],
  platform: string
): boolean {
  if (platform === Platforms.ok) {
    return checkOk(new URLSearchParams(searchOrParsedUrlQuery));
  }
  if (platform === Platforms.tg) {
    return checkTg(String(searchOrParsedUrlQuery));
  }

  return checkVk(String(searchOrParsedUrlQuery));
}

const generateHash = (secretKeys: string[], queryString: string) =>
  secretKeys.map((secretKey) =>
    crypto
      .createHmac("sha256", secretKey)
      .update(queryString)
      .digest()
      .toString("base64")
      .replace(/\+/g, "-")
      .replace(/\//g, "_")
      .replace(/=$/, "")
  );

interface ProcessedParams {
  sign: string;
  gamesSignKeys: string[];
  queryParams: QueryParam[];
}

/**
 * Функция, которая обрабатывает входящий query-параметр.
 * В случае встречи корректного в контексте подписи параметра добавляет его в массив известных параметров.
 * @param key
 * @param value
 * @param sign
 * @param gamesSignKeys
 * @param queryParams
 * @param isGames
 */
export const processQueryParam = (
  key: string,
  value: string,
  sign: string,
  gamesSignKeys: string[],
  queryParams: QueryParam[],
  isGames: boolean
): ProcessedParams => {
  if (typeof value === "string") {
    if (key === "sign") {
      sign = value;
    } else if (key === "sign_keys") {
      gamesSignKeys.push(...value.split(","));
    } else if (key.startsWith("vk_") || isGames) {
      queryParams.push({ key, value });
    }
  }

  return { sign, gamesSignKeys, queryParams };
};

// В случае с ОК берем основные параметры и генерируем md5 hash
function checkOk(params: URLSearchParams): boolean {
  /**
    MD5-хеш параметров logged_user_id+session_key+application_secret_key.
   */

  const auth_sig = params.get("auth_sig");
  const logged_user_id = params.get("logged_user_id");
  const session_key = params.get("session_key");

  if (!logged_user_id || !session_key) return false;

  const value = logged_user_id + session_key + OK_APPLICATION_SECRET_KEY;
  return crypto.createHash("md5").update(value).digest("hex") === auth_sig;
}

const checkVk = (searchOrParsedUrlQuery: string) => {
  let sign: string = "";
  let queryParams: QueryParam[] = [];

  // Проверка запускается ли приложение через ВК Игры
  const isGames =
    typeof searchOrParsedUrlQuery === "string" &&
    searchOrParsedUrlQuery.includes("sign_keys=");
  let gamesSignKeys: string[] = [];

  if (typeof searchOrParsedUrlQuery === "string") {
    // Если строка начинается с вопроса (когда передан window.location.search),
    // его необходимо удалить.
    const formattedSearch = searchOrParsedUrlQuery.startsWith("?")
      ? searchOrParsedUrlQuery.slice(1)
      : searchOrParsedUrlQuery;

    // Пытаемся спарсить строку как query-параметр.
    for (const param of formattedSearch.split("&")) {
      const array = param.split("=");
      const key = array[0];
      let value = array[1];
      if (array.length >= 2) {
        for (let i = 2; i < array.length; i++) {
          value += "=" + String(array[i]);
        }
      }

      const processedParams = processQueryParam(
        key,
        value,
        sign,
        gamesSignKeys,
        queryParams,
        isGames
      );
      sign = processedParams.sign;
      gamesSignKeys = processedParams.gamesSignKeys;
      queryParams = processedParams.queryParams;
    }
  } else {
    for (const [key, value] of Object.entries(searchOrParsedUrlQuery)) {
      const processedParams = processQueryParam(
        key,
        value,
        sign,
        gamesSignKeys,
        queryParams,
        isGames
      );
      sign = processedParams.sign;
      gamesSignKeys = processedParams.gamesSignKeys;
      queryParams = processedParams.queryParams;
    }
  }

  if (isGames && gamesSignKeys.length > 0)
    queryParams = queryParams.filter(({ key }) => gamesSignKeys.includes(key));

  // Обрабатываем исключительный случай, когда не найдена ни подпись в параметрах,
  // ни один параметр, начинающийся с "vk_", дабы избежать
  // излишней нагрузки, образующейся в процессе работы дальнейшего кода.
  if (!sign || queryParams.length === 0) {
    return false;
  }
  // Снова создаём query в виде строки из уже отфильтрованных параметров.
  const queryString = queryParams
    // Сортируем ключи в порядке возрастания.
    .sort((a, b) => a.key.localeCompare(b.key))
    // Воссоздаём новый query в виде строки.
    .reduce((acc, { key, value }, idx) => {
      return (
        acc + (idx === 0 ? "" : "&") + `${key}=${encodeURIComponent(value)}`
      );
    }, "");

  const paramHashes = generateHash(secretKeys, queryString);

  return process.env.NODE_ENV === "development"
    ? true
    : paramHashes.includes(sign);
};

// В случае с телеграммом используем встроенную библиотеку для валидации, которая по смыслу очень схожа с ОК и ВК
const checkTg = (sign: string): boolean => {
  try {
    if (enviroment.IS_PRODUCTION) {
      validate(sign, TG_BOT_TOKEN);
    }
  } catch (e) {
    throw new Error("Invalid TG signature");
  }

  const parsedInitData = initData.parse(sign);

  if (!parsedInitData.user) {
    throw new Error("User not found");
  }

  if (parsedInitData.user.isBot) {
    throw new Error("Bots is not allowed");
  }

  return true;
};
```
