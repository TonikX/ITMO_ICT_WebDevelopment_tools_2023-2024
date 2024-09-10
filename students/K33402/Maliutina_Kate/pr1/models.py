from enum import Enum
from typing import Optional, List

from sqlmodel import SQLModel, Field, Relationship


class RaceType(Enum):  # перечисление
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):  # таблица связи многие-ко-многим, унаследовано от базовой модели и помечено таблицей
    skill_id: Optional[int] = Field(default=None, foreign_key="skill.id", primary_key=True)  # поле с внешним ключом из таблицы skill, часть составного первичного ключа
    warrior_id: Optional[int] = Field(default=None, foreign_key="warrior.id", primary_key=True)  # поле с внешним ключом из таблицы skill, часть составного первичного ключа
    level: int | None  # тип данных целое число или пустота (None)


class Skill(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = ""  # опциональное строковое поле
    warriors: Optional[List["Warrior"]] = Relationship(back_populates="skills", link_model=SkillWarriorLink)
    # тип "Warrior" в кавычках, поскольку этот тип есть в файле ниже, но
    # Python интепретируемый язык и не знает, что ниже этой строчки написано
    # опциональное поле, хранящее список войнов:
    #   back_populates - ссылается на поле skills в таблице Warrior
    #   link_model - ссылка на таблицу связи многие-ко-многим


class Profession(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    description: str
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")
    # обязательное поле, хранящее список войнов - ссылается на поле profession в таблице Warrior


class WarriorDefault(SQLModel):
    race: RaceType  # поле может быть только типа RaceType - одно из значений выше
    name: str
    level: int
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")


class Warrior(WarriorDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)


# класс наследник от дефолтного войнА - служит для отображения объекта дополнительно к id
class WarriorProfessions(WarriorDefault):
    profession: Optional[Profession] = None
