# Задание №1

Подготовим коллекции базы данных для проекта.

- Users, UsersOk, UsersTg будут хранить в себе пользователей разделенных на различные платформы
- Statuses будет хранить в себе доступные для установки пользователем эмодзи-статусы
- Quests будет хранить в себе доступные для выполнения задания и условия которые необходимо выполнить для их выполнения

## Основная коллекция (hub/models/UsersVK.ts):

Начнем с User для хранения данных игрока на сервере. Т.к. игра будет работать одновременно на трех платформах, разделим пользователей на три коллекции, но, пока, не будем вносить каких-либо изменений в различные коллекции.

```typescript
import mongoose, {
  HydratedDocument,
  ObjectId,
  PopulatedDoc,
  Schema,
  Types,
  Document,
} from "mongoose";
import { IEntity } from "../../data/cards";
import { ILobby } from "../Lobbies";
import { IChestTypes } from "../../data/chests";
import { StoreProducts } from "../../data/shop";
import { MIN_RATING } from "@src/data/rating";
import { Emotions, IEmotion, PopulatedIEmotion } from "../Emotion";
import { Platforms } from "@/src/types/platforms";

export type Currency = "coins" | "voices" | "ok";

// Типизация игровых карт пользователя
export type ICard = {
  entity: IEntity;
  parts?: number;
  position?: number;
};

// Типизация игровых карт на уровне БД
const CardSchema = new Schema<ICard>({
  entity: {
    type: String,
    required: true,
  },
  parts: Number,
  position: Number,
});

// Типизация колоды эмоций у пользователя
export type IUserEmotionCard = {
  emotion: IEmotion["_id"];
  position: number | null;
};

export type IUserWithEmotions = Document<any, unknown, IUser> &
  Omit<IUser, "emotions"> & {
    emotions: mongoose.Types.Array<
      IUserEmotionCard & { emotion: PopulatedIEmotion }
    >;
  };

// Всевозможные игровые бонусы
type Bonuses = {
  daily: number;
  subGroup: boolean;
  joinChat: boolean;
  notificationApp: boolean;
  notificationBot: boolean;
  addToFavorites: boolean;
  addToHomeScreen: boolean;
  rewardedGift: {
    lastUpdate: number;
    adWatchedTimes: number;
  };
};

type Settings = {
  isMuted: boolean;
};

// Сундуки пользователя (всего 4 слота под сундуки, каждый в состоянии пустой, есть сундук, открывается и готов к открытию)
export type IChest =
  | { empty: true; _id?: ObjectId }
  | ({
      empty?: false;
      _id?: ObjectId;
      type: IChestTypes;
      adWatchedTimes: number;
    } & (
      | {
          status: "idle";
        }
      | {
          status: "opening";
          willOpenAt: number;
        }
    ));

export type IChestDocs = [
  HydratedDocument<IChest>,
  HydratedDocument<IChest>,
  HydratedDocument<IChest>,
  HydratedDocument<IChest>
];

const ChestSchema = new Schema<IChest>({
  type: String,
  status: String,
  willOpenAt: Number,
  empty: Boolean,
  adWatchedTimes: {
    type: Number,
    default: 0,
    required: true,
  },
});

// Описание эмодзи-статусов пользователя
export interface UserStatus {
  status: mongoose.Types.ObjectId;
  isSelected: boolean;
  isGiftReceived: boolean;
}

// Непосредственно интерфейс пользователя
export interface IUser {
  markModified(arg0: string): unknown;
  _id: number;
  platform: Platforms; // Указание платформы, на которой пользователь играет
  name: string;
  photo_100: string;
  photo_200: string;
  registrationDate: Date;
  ban?: boolean;
  cards: ICard[];
  emotions: IUserEmotionCard[];
  balance: number;
  history: any[];
  chests: [IChest, IChest, IChest, IChest];
  rating: number;

  stats: {
    draws: number;
    wins: number;
    losses: number;
  };
  lobby: PopulatedDoc<ILobby>;

  bonuses: Bonuses;
  isTutorialPassed: boolean;
  shop: {
    lastUpdate: number;
    boughtProducts: StoreProducts[];
    chest: {
      currency: Currency;
      chestType: IChestTypes | "";
    };

    cardFragment: {
      currency: Currency;
      card: IEntity | "";
    };
  };

  referrals: {
    refId: string;
    referralsCount: number;
  };

  statuses: UserStatus[];

  tasks: {
    current: string[];
    completed: string[];
    progress: Record<string, number>;
    nextUpdateAt: number;
    lastTasksMessageId?: number;
    madeProgress?: boolean;
  };

  settings: Settings;
}

// Колода выдаваемая по умолчанию
const defaultCards: ICard[] = [
  {
    entity: "sheep",
    position: 1,
  },
  {
    entity: "farm",
    position: 2,
  },
  {
    entity: "pasture",
    position: 3,
  },
  {
    entity: "teslaTower",
    position: 4,
  },
  {
    entity: "bigSheep",
  },
  {
    entity: "bee",
  },
  {
    entity: "doubleFarm",
    parts: 1,
  },
];

// Эмоции выдаваемые по умолчанию
const defaultEmotions: IUserEmotionCard[] = [
  { emotion: "sheepyHello", position: 1 },
  { emotion: "sheepSorry", position: 2 },
  { emotion: "sheepAngry", position: 3 },
];

export const UserSchema = new Schema<IUser>({
  _id: { index: true, required: true, type: Number },
  platform: {
    type: String,
    required: true,
    enum: Platforms,
    default: Platforms.vk,
  },
  ban: {
    type: Boolean,
    required: false,
  },
  name: {
    type: "string",
    required: true,
  },
  photo_100: {
    type: "string",
    required: true,
  },
  photo_200: {
    type: "string",
    required: true,
  },
  registrationDate: {
    type: Date,
  },
  cards: {
    type: [CardSchema],
    required: true,
    default: defaultCards,
  },
  emotions: {
    type: [
      {
        emotion: { type: String, ref: Emotions },
        position: { type: Number, default: null },
      },
    ],
    required: true,
    default: defaultEmotions,
    _id: false,
  },
  balance: {
    type: Number,
    required: true,
    default: 0,
  },
  history: {
    type: [],
    required: true,
    default: [],
  },
  stats: {
    wins: {
      type: Number,
      default: 0,
      required: true,
    },
    losses: {
      type: Number,
      default: 0,
      required: true,
    },
    draws: {
      type: Number,
      default: 0,
      required: true,
    },
  },

  chests: {
    type: [ChestSchema],
    default: [
      { empty: true },
      { empty: true },
      { empty: true },
      { empty: true },
    ],
    required: true,
  },
  rating: {
    type: Number,
    default: MIN_RATING,
    required: true,
    index: -1,
  },

  lobby: { type: Schema.Types.ObjectId, ref: "lobbies" },

  bonuses: {
    daily: {
      type: Number,
      default: 0,
      required: true,
    },
    subGroup: {
      type: Boolean,
      default: false,
      required: true,
    },
    joinChat: {
      type: Boolean,
      default: false,
      required: true,
    },
    notificationApp: {
      type: Boolean,
      default: false,
      required: true,
    },
    notificationBot: {
      type: Boolean,
      default: false,
      required: true,
    },
    addToFavorites: {
      type: Boolean,
      default: false,
      required: true,
    },
    addToHomeScreen: {
      type: Boolean,
      default: false,
      required: true,
    },
    rewardedGift: {
      lastUpdate: {
        type: Number,
        default: Date.now(),
        required: true,
      },
      adWatchedTimes: {
        type: Number,
        default: 0,
        required: true,
      },
    },
  },
  isTutorialPassed: {
    type: Boolean,
    default: false,
    required: true,
  },
  shop: {
    lastUpdate: {
      type: Number,
      default: 0,
      required: true,
    },
    boughtProducts: {
      type: Object,
      default: [],
      required: true,
    },
    chest: {
      chestType: {
        type: String,
        default: "",
      },
      currency: {
        type: String,
        default: "coins",
      },
    },
    cardFragment: {
      card: {
        type: String,
        default: "",
      },
      currency: {
        type: String,
        default: "coins",
      },
    },
  },
  tasks: {
    completed: {
      type: [String],
      required: true,
      default: [],
    },
    current: {
      type: [String],
      required: true,
      default: [],
    },
    progress: {
      type: {},
      default: {},
      required: true,
    },
    nextUpdateAt: {
      type: Number,
      required: true,
      default: 0,
    },
    lastTasksMessageId: {
      type: Number,
    },
    madeProgress: { type: Boolean },
  },

  referrals: {
    refId: {
      type: String,
      default: "",
    },
    referralsCount: {
      type: Number,
      default: 0,
    },
  },

  statuses: [
    {
      status: {
        type: Types.ObjectId,
        required: true,
        unique: false,
        ref: "emoji_status",
      },
      isGiftReceived: { type: Boolean, default: false },
      isSelected: { type: Boolean, default: false },
    },
  ],

  settings: { isMuted: { default: false, type: Boolean, required: true } },
});

// Экспортируем готовую модель
export const Users = mongoose.model("users", UserSchema);
```

## Основная коллекция (hub/models/UsersOk.ts) и (hub/models/UsersTg.ts) :

Теперь создадим дополнительные коллекции для пользователей из ТГ и ОК

```typescript
import mongoose from "mongoose";

import { UserSchema } from "./Users";

export const UsersTg = mongoose.model("userstg", UserSchema);
```

```typescript
import mongoose from "mongoose";

import { UserSchema } from "./Users";

export const UsersOk = mongoose.model("usersok", UserSchema);
```

## Коллекция доступных эмодзи-статусов (hub/models/Statuses.ts):

Отдельно объявим коллекцию для эмодзи-статусов. Чтобы связать её с пользователем. Учтем, что часть эмодзи-статусов можно будет получить выполняя различные задания.

```typescript
import mongoose, { Schema } from "mongoose";
import { IQuest } from "./Quests";
import { IChestTypes } from "@/src/data/chests";

export interface IStatus {
  _id: mongoose.Types.ObjectId;
  title: string;
  description: string;
  requiredQuest: string; // ref на quest который необходимо выполнить для разблокировки статуса
  giftChestType: IChestTypes;
  subTitle: string;
  icon: string;
  buttonText: string;
  vkStatusID: number; // id статуса в системе ВКонтакте
}

export type PopulatedIStatus = IStatus & {
  requiredQuest: IQuest;
};

const EmojiStatusSchema = new Schema<IStatus>({
  title: {
    type: String,
    required: true,
  },
  requiredQuest: {
    type: String,
    ref: "quests",
    required: true,
  },
  // Описание награды за установленный статус
  giftChestType: {
    type: String,
    enum: ["common", "magic", "legendary"],
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  subTitle: {
    type: String,
    required: true,
  },
  icon: {
    type: String,
    required: true,
  },
  buttonText: {
    type: String,
    required: true,
  },
  vkStatusID: {
    type: Number,
    required: true,
  },
});

export const EmojiStatuses = mongoose.model(
  "emoji_statuses",
  EmojiStatusSchema
);
```

## Коллекция заданий (hub/models/Quests.ts):

Спроектируем коллекцию с доступными заданиями, построим её таким образом, чтобы задания можно было использовать в различных частях приложения без особых изменений логики

```typescript
import mongoose, { Schema } from "mongoose";

/**
 * Доступные типы заданий
 */
export enum QuestType {
  INVITE_FRIENDS = "INVITE_FRIENDS",
  GAMES_COUNT = "GAMES_COUNT",
  GAMES_WINS = "GAMES_WINS",
}

export interface Requirement {
  type: QuestType;
  value: number; // Значение которого нужно добиться для выполнения задания
}

export interface IQuest {
  text: string;
  requirements: Requirement[];
}

export const QuestSchema = new Schema<IQuest>({
  text: {
    type: String,
    required: true,
  },
  requirements: {
    type: [
      {
        value: { type: Number, required: true },
        type: { type: String, enum: QuestType, required: true },
      },
    ],
  },
});

export const Quests = mongoose.model("quests", QuestSchema);
```
