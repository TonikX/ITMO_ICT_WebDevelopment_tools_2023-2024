from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    age: int

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    profile_id: Optional[int]

    class Config:
        orm_mode = True

class UserProfileBase(BaseModel):
    about_me: str

class UserProfileCreate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TripBase(BaseModel):
    destination: str
    start_date: str
    end_date: str

class TripCreate(TripBase):
    pass

class Trip(TripBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True

class TripReviewBase(BaseModel):
    rating: int
    comment: str

class TripReviewCreate(TripReviewBase):
    pass

class TripReview(TripReviewBase):
    id: int
    trip_id: int
    user_id: int

    class Config:
        orm_mode = True

class InterestBase(BaseModel):
    name: str

class InterestCreate(InterestBase):
    pass

class Interest(InterestBase):
    id: int

    class Config:
        orm_mode = True

class UserInterestBase(BaseModel):
    pass

class UserInterestCreate(UserInterestBase):
    user_id: int
    interest_id: int

class UserInterest(UserInterestBase):
    id: int
    user_id: int
    interest_id: int

    class Config:
        orm_mode = True

class PartnershipRequestBase(BaseModel):
    pass

class PartnershipRequestCreate(PartnershipRequestBase):
    trip_id: int
    user_id: int

class PartnershipRequest(PartnershipRequestBase):
    id: int
    trip_id: int
    user_id: int

    class Config:
        orm_mode = True

class PartnershipBase(BaseModel):
    pass

class PartnershipCreate(PartnershipBase):
    trip_id: int
    partner_id: int

class Partnership(PartnershipBase):
    id: int
    trip_id: int
    partner_id: int

    class Config:
        orm_mode = True
