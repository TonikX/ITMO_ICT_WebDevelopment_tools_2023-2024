import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column

VECTOR_SIZE = 312


class VisibilityEnum(str, Enum):
    public = "public"
    private = "private"


#################################################### Base classes ####################################################


class FavouriteBase(SQLModel):
    id_course: Optional[int] = Field(default=None, foreign_key="course.id")
    comment: Optional[str] = None


class UserBaseDisplay(SQLModel):
    full_name: str
    email: Optional[str] = None
    bio: Optional[str] = None


class UserBase(UserBaseDisplay):
    username: str


class UserCreate(UserBase):
    password: str


class UserWithPasswordBase(UserBase):
    hashed_password: str


class UserPasswordUpdate(SQLModel):
    old_password: str
    new_password: str


class Token(SQLModel):
    access_token: str
    token_type: str


class CourseBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_finished: bool = False
    visibility: VisibilityEnum = VisibilityEnum.public


class SectionBase(SQLModel):
    id_course: Optional[int] = Field(default=None, foreign_key="course.id")
    title: str
    description: Optional[str] = None


class TopicBase(SQLModel):
    id_section: Optional[int] = Field(default=None, foreign_key="section.id")
    title: str
    description: Optional[str] = None


######################### Table classes with primary keys, some matadata and NO relationships #########################


class FavouriteWithPK(FavouriteBase):
    id: int = Field(default=None, primary_key=True)
    date_added: Optional[datetime.datetime] = None


class UserWithPK(UserWithPasswordBase):
    id: int = Field(default=None, primary_key=True)
    disabled: bool = False
    date_joined: Optional[datetime.datetime] = None


class CourseWithPK(CourseBase):
    id: int = Field(default=None, primary_key=True)


class CourseWithPKExt(CourseWithPK):
    date_created: Optional[datetime.datetime] = None
    # vector: List[float] = Field(sa_column=Column(Vector(VECTOR_SIZE)))  TODO: add vector similarity search


class SectionWithPK(SectionBase):
    id: int = Field(default=None, primary_key=True)
    num_in_course: int


class TopicWithPK(TopicBase):
    id: int = Field(default=None, primary_key=True)
    num_in_section: int


########################################### Table classes with relationships ##########################################


class Favourite(FavouriteWithPK, table=True):
    id_user: Optional[int] = Field(default=None, foreign_key="user.id")


class User(UserWithPK, table=True):
    courses: List["Course"] = Relationship(back_populates="creator")
    favorite_courses: List["Course"] = Relationship(
        back_populates="liked_by", sa_relationship_kwargs={"cascade": "all, delete"}, link_model=Favourite
    )


class Course(CourseWithPKExt, table=True):
    id_creator: Optional[int] = Field(default=None, foreign_key="user.id")
    creator: "User" = Relationship(back_populates="courses")
    liked_by: List["User"] = Relationship(back_populates="favorite_courses", link_model=Favourite)
    sections: List["Section"] = Relationship(back_populates="course", sa_relationship_kwargs={"cascade": "all, delete"})


class Section(SectionWithPK, table=True):
    course: "Course" = Relationship(back_populates="sections")
    topics: List["Topic"] = Relationship(back_populates="section", sa_relationship_kwargs={"cascade": "all, delete"})


class Topic(TopicWithPK, table=True):
    section: "Section" = Relationship(back_populates="topics")


####################################### Weird things needed because I am stupid #######################################


class SectionDisplay(SectionWithPK):
    topics: List[Topic]  # to preserve nested view


class CourseDisplay(CourseWithPK):
    sections: List[SectionDisplay]  # to preserve nested view


class CourseDisplayWithCreator(CourseDisplay):
    creator: UserBaseDisplay


class CourseDisplayWithCreatorAndComment(CourseDisplayWithCreator):
    comment: Optional[str] = None
