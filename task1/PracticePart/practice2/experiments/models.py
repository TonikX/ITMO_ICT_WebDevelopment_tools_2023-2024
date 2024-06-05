from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum

class RaceType(Enum):
    director = "director"
    worker = "worker"
    junior = "junior"


class SkillWarriorLink(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    skill_id: int = Field(foreign_key="skill.id")
    warrior_id: int= Field(foreign_key="warrior.id")
    level: Optional[int]


class BaseSkill(SQLModel):
    name: str
    description: str


class Skill(BaseSkill, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors: Optional[List['Warrior']] = Relationship(back_populates='skills', link_model=SkillWarriorLink)


class BaseProfession(SQLModel):
    title: str
    description: str


class Profession(BaseProfession, table=True):
    id: int = Field(default=None, primary_key=True)
    warriors_prof: List["Warrior"] = Relationship(back_populates="profession")


class BaseWarrior(SQLModel):
    race: RaceType
    name: str
    level: int


class Warrior(BaseWarrior, table=True):
    id: int = Field(default=None, primary_key=True)
    profession_id: Optional[int] = Field(default=None, foreign_key="profession.id")
    profession: Optional[Profession] = Relationship(back_populates="warriors_prof")
    skills: Optional[List[Skill]] = Relationship(back_populates="warriors", link_model=SkillWarriorLink)


class WarriorProfessions(BaseWarrior):
    profession: Optional[Profession] = None


class WarriorUpdate(SQLModel):
    race: Optional[RaceType] = None
    name: Optional[str] = None
    level: Optional[int] = None
    profession_id: Optional[int] = None
