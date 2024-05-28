from datetime import datetime, date
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
from pydantic import validator

# Enum
class Gender(Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"

class RequestStatus(Enum):
    Pending = "Pending"
    Accepted = "Accpeted"
    Rejected = "Rejected"

class TripStatus(Enum):
    Canceled = "canceled"
    Ongoing = "on going"
    Completed = "completed"

# Link
class TripUserLink(SQLModel, table=True):
    trip_id: Optional[int] = Field(default=None, foreign_key="trip.id", primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", primary_key=True)    

# User models
class UserDefault(SQLModel):
    username: str
    email: str
    password: str
    
class User(UserDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    trips: Optional[List["Trip"]] = Relationship(back_populates="users", link_model=TripUserLink)
    user_profile: Optional["UserProfile"] = Relationship(back_populates="user")
    trip_request: Optional[List["TripRequest"]] = Relationship(back_populates="user_request")

class UserInput(SQLModel):
    username: str
    email: str
    password: str = Field(max_length=256, min_length=6)
    password2: str

    @validator('password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('password doesn\'t match')
        return v
    
class UserChangePassWord(SQLModel):
    old_password: str
    new_password: str = Field(max_length=256, min_length=6)
    new_password2: str

    @validator('new_password2')
    def password_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('password doesn\'t match')
        return v

class UserLogin(SQLModel):
    username: str
    password: str

# Profile models
class UserProfileDefault(SQLModel):
    full_name: str
    age: int
    gender: Gender
    address: str
    skills: Optional[str] = ""
    travel_experience: Optional[str] = ""
    hobby: Optional[str] = ""
    
class UserProfile(UserProfileDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="user_profile")
    reviews: Optional[List["UserReview"]] = Relationship(back_populates="user_profile")

class Profile_User(UserDefault):
    profile: Optional[UserProfile] = None

# Review models
class UserReviewDefault(SQLModel):
    review_content: str
    
class UserReview(UserReviewDefault, table=True):
    id: int = Field(default=None, primary_key=True)
    reviewer: str
    review_time: date
    user_profile_id: int = Field(foreign_key="userprofile.id")
    user_profile: Optional[UserProfile] = Relationship(back_populates="reviews")

class ProfileReviews(UserProfileDefault):
    reviews: Optional[List[UserReview]] = None

# Trip models
class TripDefault(SQLModel):
    departure: str
    destination: str
    date_start: date
    date_end: date
    estimated_cost: float
    trip_status: TripStatus
    other_details: Optional[str] = ""

class Trip(TripDefault, table=True):
    id: int = Field(default=None, primary_key=True)

    users: Optional[List[User]] = Relationship(back_populates="trips", link_model=TripUserLink)
    requests: Optional[List["TripRequest"]] = Relationship(back_populates="trip")

class TripRequestDefault(SQLModel):
    message: Optional[str] = ""
    request_status: RequestStatus

    trip_id: int = Field(foreign_key="trip.id")
    

class TripRequest(TripRequestDefault, table=True):
    id: int = Field(default=None, primary_key=True)
 
    user_request_id: int = Field(foreign_key="user.id")
    trip: Optional[Trip] = Relationship(back_populates="requests")
    user_request: Optional[User] = Relationship(back_populates="trip_request")

class TripUsers(SQLModel):
    trip: Trip
    users: Optional[List[str]] = None




