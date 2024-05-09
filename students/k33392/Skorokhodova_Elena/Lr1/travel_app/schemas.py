from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(String)
    skills = Column(String)
    experience = Column(String)
    preferences = Column(String)
    user = relationship("User", back_populates="profile")


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    departure_location = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    duration = Column(Integer)
    details = Column(String)

    owner = relationship("User", back_populates="trips")
    users = relationship("UserProfile", secondary="user_trips", back_populates="trip")
    reviews = relationship("TripReview", back_populates="trip")


class UserTrip(Base):
    __tablename__ = "user_trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    trip_id = Column(Integer, ForeignKey("trips.id"))
    role = Column(String)


class TripReview(Base):
    __tablename__ = "trip_reviews"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer)
    comment = Column(String)

    user = relationship("User")
    trip = relationship("Trip", back_populates="reviews")


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserProfileBase(BaseModel):
    username: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    preferences: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class TripBase(BaseModel):
    owner_id: int
    departure_location: str
    destination: str
    start_date: datetime
    end_date: datetime
    duration: int
    details: Optional[str] = None


class TripCreate(TripBase):
    pass


class TripUpdate(TripBase):
    pass


class UserTripBase(BaseModel):
    user_id: int
    trip_id: int
    role: Optional[str] = None


class UserTripCreate(UserTripBase):
    pass


class TripReviewBase(BaseModel):
    trip_id: int
    user_id: int
    rating: int
    comment: Optional[str] = None


class TripReviewCreate(TripReviewBase):
    pass
