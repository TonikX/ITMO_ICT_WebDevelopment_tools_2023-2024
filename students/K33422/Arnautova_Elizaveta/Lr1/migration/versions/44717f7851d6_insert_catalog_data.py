"""insert catalog data

Revision ID: 44717f7851d6
Revises: 9f30b9fc302a
Create Date: 2024-05-19 11:56:57.916707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Table, MetaData
from database import engine

import models

# revision identifiers, used by Alembic.
revision: str = '44717f7851d6'
down_revision: Union[str, None] = '9f30b9fc302a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

meta = MetaData()
region = Table('region', meta, autoload_with=engine)
place = Table('place', meta, autoload_with=engine)


def upgrade() -> None:
    op.bulk_insert(
        region,
        [
            {
                "id": 1,
                "name": "Центральная Россия"
            },
            {
                "id": 2,
                "name": "Восточная Россия"
            },
            {
                "id": 3,
                "name": "Дальневосточная Россия"
            },
            {
                "id": 4,
                "name": "Восточная Европа"
            },
            {
                "id": 5,
                "name": "Западная Европа"
            },
            {
                "id": 6,
                "name": "Ближний Восток"
            },
            {
                "id": 7,
                "name": "Средняя Азия"
            },
            {
                "id": 8,
                "name": "Юго-Восточная Азия"
            },
            {
                "id": 9,
                "name": "Южная Азия"
            },
            {
                "id": 10,
                "name": "Океания"
            },
            {
                "id": 11,
                "name": "Северная Африка"
            },
            {
                "id": 12,
                "name": "Центральная Африка"
            },
            {
                "id": 13,
                "name": "Южная Африка"
            },
            {
                "id": 14,
                "name": "Северная Америка"
            },
            {
                "id": 15,
                "name": "Центральная Америка"
            },
            {
                "id": 16,
                "name": "Южная Америка"
            },
            {
                "id": 17,
                "name": "Арктика"
            },
            {
                "id": 18,
                "name": "Антарктика"
            },
        ],
        multiinsert=False,
    )
    op.bulk_insert(place,
                   [
                       {
                           "name": "Москва",
                           "region_id": 1
                       },
                       {
                           "name": "Санкт-Петербург",
                           "region_id": 1
                       },
                       {
                           "name": "Нижний Новгород",
                           "region_id": 1
                       },
                       {
                           "name": "Волгоград",
                           "region_id": 1
                       },
                       {
                           "name": "Омск",
                           "region_id": 2
                       },
                       {
                           "name": "Пермь",
                           "region_id": 2
                       },
                       {
                           "name": "Челябинск",
                           "region_id": 2
                       },
                       {
                           "name": "Екатеринбург",
                           "region_id": 2
                       },
                       {
                           "name": "Петропавловск-Камчатский",
                           "region_id": 3
                       },
                       {
                           "name": "Владивосток",
                           "region_id": 3
                       },
                       {
                           "name": "Южно-Сахалинск",
                           "region_id": 3
                       },
                       {
                           "name": "Магадан",
                           "region_id": 3
                       },
                       {
                           "name": "Минск",
                           "region_id": 4
                       },
                       {
                           "name": "Варшава",
                           "region_id": 4
                       },
                       {
                           "name": "Вильнюс",
                           "region_id": 4
                       },
                       {
                           "name": "Лондон",
                           "region_id": 5
                       },
                       {
                           "name": "Берлин",
                           "region_id": 5
                       },
                       {
                           "name": "Мадрид",
                           "region_id": 5
                       },
                       {
                           "name": "Стамбул",
                           "region_id": 6
                       },
                       {
                           "name": "Тель-Авив",
                           "region_id": 6
                       },
                       {
                           "name": "Доха",
                           "region_id": 6
                       },
                       {
                           "name": "Ташкент",
                           "region_id": 7
                       },
                       {
                           "name": "Астана",
                           "region_id": 7
                       },
                       {
                           "name": "Душанбе",
                           "region_id": 7
                       },
                       {
                           "name": "Куала-Лумпур",
                           "region_id": 8
                       },
                       {
                           "name": "Бангкок",
                           "region_id": 8
                       },
                       {
                           "name": "Сингапур",
                           "region_id": 8
                       },
                       {
                           "name": "Шри-Ланка",
                           "region_id": 9
                       },
                       {
                           "name": "Непал",
                           "region_id": 9
                       },
                       {
                           "name": "Нью-Дели",
                           "region_id": 9
                       },
                       {
                           "name": "Сидней",
                           "region_id": 10
                       },
                       {
                           "name": "Окленд",
                           "region_id": 10
                       },
                       {
                           "name": "Каир",
                           "region_id": 11
                       },
                       {
                           "name": "Тунис",
                           "region_id": 11
                       },
                       {
                           "name": "Ангола",
                           "region_id": 12
                       },
                       {
                           "name": "Чад",
                           "region_id": 12
                       },
                       {
                           "name": "Мадагаскар",
                           "region_id": 13
                       },
                       {
                           "name": "Мозамбик",
                           "region_id": 13
                       },
                       {
                           "name": "Лос-Анжелес",
                           "region_id": 14
                       },
                       {
                           "name": "Торонто",
                           "region_id": 14
                       },
                       {
                           "name": "Гондурас",
                           "region_id": 15
                       },
                       {
                           "name": "Панама",
                           "region_id": 15
                       },
                       {
                           "name": "Чили",
                           "region_id": 16
                       },
                       {
                           "name": "Перу",
                           "region_id": 16
                       },
                       {
                           "name": "о. Шпицберген",
                           "region_id": 17
                       },
                       {
                           "name": "Географический южный полюс",
                           "region_id": 18
                       },
                   ],
                   multiinsert=False,
                   )


def downgrade() -> None:
    models.Place.query.delete()
    models.Region.query.delete()
