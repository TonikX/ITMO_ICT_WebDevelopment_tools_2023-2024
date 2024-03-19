from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    username: str
    email: str
    trips: List["Trip"] = Relationship(back_populates="user")
    first_name: str
    last_name: str
    age: int
    profile: Optional["UserProfile"] = Relationship(back_populates="user")

    class Config:
        from_attributes = True

class UserProfile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Добавляем внешний ключ
    about_me: str
    user: Optional[User] = Relationship(back_populates="profile")

class Trip(SQLModel, table=True):
    id: int = Field(primary_key=True)
    destination: str
    start_date: str
    end_date: str
    user_id: int = Field(foreign_key="user.id")  # Добавляем внешний ключ
    user: Optional[User] = Relationship(back_populates="trips")
    reviews: List["TripReview"] = Relationship(back_populates="trip")

class TripReview(SQLModel, table=True):
    id: int = Field(primary_key=True)
    trip_id: int = Field(foreign_key="trip.id")  # Добавляем внешний ключ
    user_id: int = Field(foreign_key="user.id")  # Добавляем внешний ключ
    rating: int
    comment: str
    user: Optional[User] = Relationship(back_populates="reviews")
    trip: Optional[Trip] = Relationship(back_populates="reviews")

class Interest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    users: List["User"] = Relationship(back_populates="interests")

class UserInterest(SQLModel, table=True):
    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="user.id")  # Добавляем внешний ключ
    interest_id: int = Field(foreign_key="interest.id")  # Добавляем внешний ключ
    user: Optional[User] = Relationship(back_populates="user_interests")
    interest: Optional[Interest] = Relationship(back_populates="user_interests")
