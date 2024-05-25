from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    personal_information = Column(String)
    travelling_skills = Column(String)
    personal_transport = Column(String)
    companion_preferences = Column(String)

    owned_trips = relationship('Trip', foreign_keys='Trip.initiator_id', back_populates='initiator')


class Trip(Base):
    __tablename__ = 'trip'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    initiator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    companion_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(Date)
    expected_end_date = Column(Date)
    is_completed = Column(Boolean)
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    place_id = Column(Integer, ForeignKey('place.id'))

    initiator = relationship('User', foreign_keys=[initiator_id])
    companion = relationship('User', foreign_keys=[companion_id])
    region = relationship('Region', foreign_keys=[region_id])
    place = relationship('Place', foreign_keys=[place_id])
    requests = relationship('TripJoinRequest', back_populates='trip')


class Region(Base):
    __tablename__ = 'region'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    places = relationship('Place', back_populates='region')


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('region.id'))

    region = relationship('Region', back_populates='places')


class Swipe(Base):
    __tablename__ = 'swipe'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    is_right = Column(Boolean, nullable=False)

    __table_args__ = (UniqueConstraint('sender_id', 'recipient_id'),)


class TripJoinRequest(Base):
    __tablename__ = 'trip_join_request'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    trip_id = Column(Integer, ForeignKey('trip.id'), nullable=False)
    accepted = Column(Boolean)

    trip = relationship('Trip', back_populates='requests')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    recipient_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
