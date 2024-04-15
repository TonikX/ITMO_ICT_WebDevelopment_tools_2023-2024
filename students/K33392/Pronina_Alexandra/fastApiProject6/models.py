from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    profile_id = Column(Integer, ForeignKey('user_profiles.id'))
    profile = relationship("UserProfile", back_populates="user")
    trips = relationship("Trip", back_populates="user")
    reviews = relationship("TripReview", back_populates="user")
    interests = relationship("UserInterest", back_populates="user")
    partnership_requests = relationship("PartnershipRequest", back_populates="user")
    partners = relationship("Partnership", back_populates="partner")

class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True, index=True)
    about_me = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="profile")

class Trip(Base):
    __tablename__ = 'trips'
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="trips")
    reviews = relationship("TripReview", back_populates="trip")

class TripReview(Base):
    __tablename__ = 'trip_reviews'
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)
    comment = Column(Text)
    user = relationship("User", back_populates="reviews")
    trip = relationship("Trip", back_populates="reviews")

class Interest(Base):
    __tablename__ = 'interests'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    users = relationship("UserInterest", back_populates="interest")

class UserInterest(Base):
    __tablename__ = 'user_interests'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    interest_id = Column(Integer, ForeignKey('interests.id'))
    user = relationship("User", back_populates="interests")
    interest = relationship("Interest", back_populates="users")

class PartnershipRequest(Base):
    __tablename__ = 'partnership_requests'
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    trip = relationship("Trip", back_populates="partnership_requests")
    user = relationship("User", back_populates="partnership_requests")

class Partnership(Base):
    __tablename__ = 'partnerships'
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    partner_id = Column(Integer, ForeignKey('users.id'))
    trip = relationship("Trip", back_populates="partners")
    partner = relationship("User", back_populates="partners")
